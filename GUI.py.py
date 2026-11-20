
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QComboBox, QLineEdit, QGroupBox,
    QHeaderView, QTextEdit
)

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from source.banker_engine import chay_banker, resource_request
from source.deadlock_engine import detect_deadlock


class ResourceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OS Resource Manager | Banker & Deadlock")
        self.resize(1280, 850)
        self.state = None
        self.original_state = None
        self.current_file = None
        self.last_result = {}
        self._build_ui()
        self._set_style()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)

        header = QHBoxLayout()
        title = QLabel("OS RESOURCE MANAGER")
        title.setObjectName("title")
        self.file_label = QLabel("Chưa chọn dữ liệu CSV")
        btn_load = QPushButton("Chọn CSV")
        btn_load.clicked.connect(self.load_csv)
        btn_reset = QPushButton("Đặt lại (Reset)")
        btn_reset.clicked.connect(self.reset_state)
        btn_log = QPushButton("Lưu Log")
        btn_log.clicked.connect(self.save_log)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.file_label)
        header.addWidget(btn_load)
        header.addWidget(btn_reset)
        header.addWidget(btn_log)
        root_layout.addLayout(header)

        grid = QGridLayout()
        self.tables = {}
        for idx, name in enumerate(["Allocation", "Max", "Available", "Need"]):
            group = QGroupBox(name)
            layout = QVBoxLayout(group)
            table = QTableWidget()
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            table.verticalHeader().setVisible(False)
            table.setAlternatingRowColors(True)
            table.setMinimumHeight(230)
            layout.addWidget(table)
            self.tables[name] = table
            grid.addWidget(group, idx // 2, idx % 2)
        root_layout.addLayout(grid)

        request_group = QGroupBox("RESOURCE REQUEST (BANKER)")
        request_layout = QHBoxLayout(request_group)
        request_layout.addWidget(QLabel("Tiến trình:"))
        self.process_combo = QComboBox()
        request_layout.addWidget(self.process_combo)
        request_layout.addWidget(QLabel("Vector yêu cầu (cách nhau bằng dấu phẩy):"))
        self.request_input = QLineEdit()
        self.request_input.setPlaceholderText("Ví dụ: 1,0,2")
        request_layout.addWidget(self.request_input, 1)
        btn_request = QPushButton("Gửi yêu cầu")
        btn_request.clicked.connect(self.submit_request)
        request_layout.addWidget(btn_request)
        root_layout.addWidget(request_group)

        actions = QHBoxLayout()
        btn_banker = QPushButton("Chạy Safety Check")
        btn_banker.clicked.connect(self.run_banker)
        btn_deadlock = QPushButton("Detect Deadlock")
        btn_deadlock.clicked.connect(self.run_deadlock)
        actions.addWidget(btn_banker)
        actions.addWidget(btn_deadlock)
        actions.addStretch()
        root_layout.addLayout(actions)

        self.result_label = QLabel("Kết quả: Chưa chạy thuật toán")
        self.result_label.setObjectName("result")
        root_layout.addWidget(self.result_label)
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setPlaceholderText("Nhật ký thao tác và kết quả thuật toán...")
        self.log_view.setMaximumHeight(150)
        root_layout.addWidget(self.log_view)

    def _set_style(self):
        self.setStyleSheet("""
            QMainWindow { background: #f3f6fb; }
            QLabel#title { font-size: 22px; font-weight: 700; color: #17365d; }
            QGroupBox { font-weight: 700; border: 1px solid #cbd5e1; border-radius: 8px; margin-top: 10px; padding-top: 10px; background: white; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
            QPushButton { background: #2457a7; color: white; border: 0; border-radius: 5px; padding: 8px 13px; font-weight: 600; }
            QPushButton:hover { background: #17417f; }
            QLineEdit, QComboBox { padding: 7px; border: 1px solid #cbd5e1; border-radius: 5px; background: white; }
            QTableWidget { background: white; gridline-color: #dbe3ee; }
            QLabel#result { font-size: 15px; font-weight: 700; padding: 8px; }
        """)

    def _log(self, message):
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_view.append(f"[{stamp}] {message}")

    def _parse_csv(self, path):
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError("File CSV rỗng hoặc thiếu tiêu đề.")
            rows = list(reader)
        if not rows:
            raise ValueError("CSV không có dữ liệu.")

        headers = set(reader.fieldnames)
        required = {"Process", "Allocation_A", "Allocation_B", "Allocation_C"}
        if not required.issubset(headers):
            raise ValueError("CSV thiếu cột Process hoặc Allocation_A/B/C.")

        processes, allocation, maximum, requests = [], [], [], []
        available = None
        is_deadlock = all(f"Request_{r}" in headers for r in "ABC")
        for row in rows:
            pid = (row.get("Process") or "").strip()
            if not pid:
                continue
            if pid.upper() == "AVAILABLE":
                available = [self._to_int(row.get(f"Allocation_{r}"), f"Available {r}") for r in "ABC"]
                continue
            processes.append(pid)
            allocation.append([self._to_int(row.get(f"Allocation_{r}"), f"{pid} Allocation {r}") for r in "ABC"])
            if is_deadlock:
                requests.append([self._to_int(row.get(f"Request_{r}"), f"{pid} Request {r}") for r in "ABC"])
                maximum.append([0, 0, 0])
            else:
                maximum.append([self._to_int(row.get(f"Max_{r}"), f"{pid} Max {r}") for r in "ABC"])
        if not processes:
            raise ValueError("Không tìm thấy tiến trình P0, P1,... trong CSV.")
        if available is None:
            raise ValueError("Thiếu dòng AVAILABLE.")
        if any(v < 0 for row in allocation + maximum for v in row) or any(v < 0 for v in available):
            raise ValueError("Không được nhập số âm.")
        if not is_deadlock:
            if any(allocation[i][j] > maximum[i][j] for i in range(len(processes)) for j in range(3)):
                raise ValueError("Allocation không được lớn hơn Max.")
            need = [[maximum[i][j] - allocation[i][j] for j in range(3)] for i in range(len(processes))]
        else:
            need = [[0, 0, 0] for _ in processes]
        return {
            "processes": processes, "allocation": allocation, "max": maximum,
            "available": available, "need": need, "request": requests,
            "mode": "deadlock" if is_deadlock else "banker"
        }

    @staticmethod
    def _to_int(value, label):
        try:
            if value is None or str(value).strip() == "":
                raise ValueError
            number = int(str(value).strip())
            return number
        except (ValueError, TypeError):
            raise ValueError(f"{label}: phải là số nguyên hợp lệ.")

    def load_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Chọn file CSV", str(ROOT / "data"), "CSV files (*.csv)")
        if not path:
            return
        try:
            self.state = self._parse_csv(path)
            self.original_state = json.loads(json.dumps(self.state))
            self.current_file = path
            self._refresh()
            self.file_label.setText(Path(path).name)
            self.result_label.setText("Kết quả: Đã nạp dữ liệu thành công")
            self._log(f"Đã nạp {Path(path).name} ({len(self.state['processes'])} tiến trình).")
        except Exception as exc:
            QMessageBox.critical(self, "Lỗi dữ liệu CSV", str(exc))

    def _fill_table(self, table, row_labels, col_labels, matrix):
        table.clear()
        table.setRowCount(len(row_labels))
        table.setColumnCount(len(col_labels))
        table.setHorizontalHeaderLabels(col_labels)
        table.setVerticalHeaderLabels(row_labels)
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(i, j, item)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def _refresh(self):
        if not self.state:
            return
        s = self.state
        pids = s["processes"]
        resources = ["A", "B", "C"]
        self._fill_table(self.tables["Allocation"], pids, resources, s["allocation"])
        self._fill_table(self.tables["Max"], pids, resources, s["max"])
        self._fill_table(self.tables["Available"], ["Available"], resources, [s["available"]])
        self._fill_table(self.tables["Need"], pids, resources, s["need"])
        self.process_combo.clear()
        self.process_combo.addItems(pids)

    def run_banker(self):
        if not self.state:
            QMessageBox.warning(self, "Chưa có dữ liệu", "Vui lòng chọn file CSV trước.")
            return
        if self.state["mode"] != "banker":
            QMessageBox.warning(self, "Sai loại dữ liệu", "Safety Check cần CSV có các cột Max_A, Max_B, Max_C.")
            return
        s = self.state
        result = chay_banker(s["processes"], s["allocation"], s["max"], s["available"])
        self.last_result = {"type": "BANKER", **result}
        self.result_label.setText(f"Kết quả: {result['status']} | Safe Sequence: {' → '.join(result['safe_sequence']) or 'Không có'}")
        self._log(f"Banker: {result['status']}; Safe Sequence={result['safe_sequence']}; tiến trình chưa hoàn tất={result['unallocated_processes']}.")

    def submit_request(self):
        if not self.state:
            QMessageBox.warning(self, "Chưa có dữ liệu", "Vui lòng chọn file Banker CSV trước.")
            return
        if self.state["mode"] != "banker":
            QMessageBox.warning(self, "Sai loại dữ liệu", "Resource Request chỉ áp dụng với dữ liệu Banker.")
            return
        raw = self.request_input.text().strip()
        try:
            parts = [x.strip() for x in raw.split(",")]
            if len(parts) != len(self.state["available"]) or any(x == "" for x in parts):
                raise ValueError("Vector yêu cầu phải có đúng 3 số, ví dụ: 1,0,2.")
            request = [int(x) for x in parts]
            if any(x < 0 for x in request):
                raise ValueError("Request không được chứa số âm.")
            pid_index = self.process_combo.currentIndex()
            if pid_index < 0:
                raise ValueError("Vui lòng chọn tiến trình.")
            s = self.state
            result = resource_request(pid_index, request, s["allocation"], s["max"], s["available"])
            self.last_result = {"type": "RESOURCE_REQUEST", **result}
            self._log(f"Request {s['processes'][pid_index]} {request}: {result['status']} - {result['message']}")
            if result["status"] == "GRANTED":
                s["allocation"][pid_index] = [s["allocation"][pid_index][j] + request[j] for j in range(3)]
                s["available"] = list(result["available"])
                s["need"] = [[s["max"][i][j] - s["allocation"][i][j] for j in range(3)] for i in range(len(s["processes"]))]
                self._refresh()
                self.result_label.setText(f"Kết quả: GRANTED | SAFE | {' → '.join(result['safe_sequence'])}")
                self.request_input.clear()
                QMessageBox.information(self, "Chấp nhận yêu cầu", result["message"])
            else:
                self.result_label.setText(f"Kết quả: {result['status']} | {result['message']}")
                QMessageBox.warning(self, "Yêu cầu không được cấp", result["message"])
        except ValueError as exc:
            QMessageBox.critical(self, "Request không hợp lệ", str(exc) if str(exc) else "Request phải gồm các số nguyên.")

    def run_deadlock(self):
        if not self.state:
            QMessageBox.warning(self, "Chưa có dữ liệu", "Vui lòng chọn file CSV trước.")
            return
        if self.state["mode"] != "deadlock":
            QMessageBox.warning(self, "Sai loại dữ liệu", "Detect Deadlock cần CSV có các cột Request_A, Request_B, Request_C.")
            return
        s = self.state
        result = detect_deadlock(s["allocation"], s["request"], s["available"])
        self.last_result = {"type": "DEADLOCK", **result}
        if result["deadlocked_pids"]:
            self.result_label.setText("Kết quả: DEADLOCK | " + ", ".join(result["deadlocked_pids"]))
        else:
            self.result_label.setText("Kết quả: SAFE | " + " → ".join(result["safe_sequence"]))
        self._log(f"Deadlock Detection: {result['status']}; deadlocked={result['deadlocked_pids']}; safe sequence={result['safe_sequence']}.")

    def reset_state(self):
        if not self.original_state:
            QMessageBox.information(self, "Reset", "Chưa có dữ liệu gốc để khôi phục.")
            return
        self.state = json.loads(json.dumps(self.original_state))
        self._refresh()
        self.last_result = {}
        self.result_label.setText("Kết quả: Đã khôi phục ma trận gốc.")
        self._log("Đã Reset về dữ liệu CSV ban đầu.")

    def save_log(self):
        os.makedirs(ROOT / "output", exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = ROOT / "output" / f"gui_log_{stamp}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.log_view.toPlainText())
            if self.last_result:
                f.write("\n\nKET QUA CUOI:\n")
                f.write(json.dumps(self.last_result, ensure_ascii=False, indent=2, default=str))
        QMessageBox.information(self, "Lưu Log", f"Đã lưu log tại:\n{path}")
        self._log(f"Đã lưu log: {path.name}")


def main():
    app = QApplication(sys.argv)
    window = ResourceApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
