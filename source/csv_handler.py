import csv
import os


class CSVValidationError(Exception):
    pass


def calculate_need(allocation, max_need):
    need = []
    for i in range(len(allocation)):
        row = []
        for j in range(len(allocation[i])):
            value = max_need[i][j] - allocation[i][j]
            if value < 0:
                raise CSVValidationError(
                    f"Dữ liệu không hợp lệ: Allocation > Max tại tiến trình thứ {i + 1}"
                )
            row.append(value)
        need.append(row)
    return need


def doc_file_csv(file_path):
    """
    Đọc và kiểm tra hợp lệ file CSV.
    Hỗ trợ tự động cả 2 định dạng của nhóm:
    - Format 1 (Benchmark của Khang): PID, Alloc_R1..Rn, Max_R1..Rn, Avail_R1..Rn (Avail chỉ ghi ở dòng đầu, các dòng sau để trống)
    - Format 2 (Oracle của Vinh): Process, Allocation_A/B/C, Max_A/B/C + dòng AVAILABLE ở cuối
    """
    if not os.path.exists(file_path):
        raise CSVValidationError("Không tìm thấy file CSV.")

    if os.path.getsize(file_path) == 0:
        raise CSVValidationError("File CSV rỗng.")

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = list(csv.reader(file))

    if len(reader) < 2:
        raise CSVValidationError("File CSV thiếu dữ liệu tiến trình.")

    header = [col.strip() for col in reader[0]]
    allocation = []
    max_need = []
    processes = []
    available = None

    try:
        # TRƯỜNG HỢP 1: Format Benchmark của Khang (cột Avail_ nằm ngang trên header)
        if any(col.startswith("Avail_") for col in header):
            num_res = (len(header) - 1) // 3
            if num_res <= 0:
                raise CSVValidationError("Cấu trúc cột file Benchmark không hợp lệ.")

            for idx, row in enumerate(reader[1:], start=2):
                if not row or all(cell.strip() == "" for cell in row):
                    continue
                if len(row) < 1 + num_res * 2:
                    raise CSVValidationError(f"Thiếu cột dữ liệu ở dòng {idx}.")

                pid = row[0].strip()
                # Chỉ ép kiểu 2*num_res cột đầu (Alloc và Max)
                alloc_max_vals = [int(x.strip()) for x in row[1 : 1 + num_res * 2]]
                if any(v < 0 for v in alloc_max_vals):
                    raise CSVValidationError(f"Phát hiện giá trị âm ở tiến trình {pid}.")

                processes.append(pid)
                allocation.append(alloc_max_vals[0:num_res])
                max_need.append(alloc_max_vals[num_res : num_res * 2])

                # Lấy Available từ dòng đầu tiên có dữ liệu Avail (bỏ qua các dòng để trống ,,,,,)
                if available is None and len(row) >= 1 + num_res * 3:
                    avail_raw = [x.strip() for x in row[1 + num_res * 2 : 1 + num_res * 3]]
                    if all(x != "" for x in avail_raw):
                        avail_vals = [int(x) for x in avail_raw]
                        if any(v < 0 for v in avail_vals):
                            raise CSVValidationError("Giá trị Available không được âm.")
                        available = avail_vals

        # TRƯỜNG HỢP 2: Format Oracle của Vinh (dòng AVAILABLE nằm dưới cùng)
        elif "Allocation_A" in header:
            col_idx = {name: i for i, name in enumerate(header)}
            required = ["Process", "Allocation_A", "Allocation_B", "Allocation_C"]
            for req in required:
                if req not in col_idx:
                    raise CSVValidationError(f"Thiếu cột bắt buộc: {req}")

            has_max = all(k in col_idx for k in ["Max_A", "Max_B", "Max_C"])

            for idx, row in enumerate(reader[1:], start=2):
                if not row or all(cell.strip() == "" for cell in row):
                    continue
                pid = row[col_idx["Process"]].strip()

                alloc = [
                    int(row[col_idx["Allocation_A"]].strip()),
                    int(row[col_idx["Allocation_B"]].strip()),
                    int(row[col_idx["Allocation_C"]].strip()),
                ]
                if any(v < 0 for v in alloc):
                    raise CSVValidationError(f"Phát hiện giá trị âm ở dòng {idx}.")

                if pid.upper() == "AVAILABLE":
                    available = alloc
                    continue

                if has_max:
                    max_row = [
                        int(row[col_idx["Max_A"]].strip()),
                        int(row[col_idx["Max_B"]].strip()),
                        int(row[col_idx["Max_C"]].strip()),
                    ]
                    if any(v < 0 for v in max_row):
                        raise CSVValidationError(f"Phát hiện giá trị Max âm ở {pid}.")
                else:
                    max_row = alloc[:]

                processes.append(pid)
                allocation.append(alloc)
                max_need.append(max_row)
        else:
            raise CSVValidationError("Định dạng header CSV không được hỗ trợ.")

    except ValueError:
        raise CSVValidationError("File CSV chứa ký tự chữ cái hoặc số không phải số nguyên.")

    if len(processes) == 0:
        raise CSVValidationError("Không có tiến trình nào trong file.")
    if available is None:
        raise CSVValidationError("Thiếu thông tin tài nguyên khả dụng (AVAILABLE).")

    need = calculate_need(allocation, max_need)

    return {
        "processes": processes,
        "allocation": allocation,
        "max": max_need,
        "available": available,
        "need": need,
    }


def ghi_file_csv(ten_file, status, ket_qua):
    """Ghi kết quả thực thi ra thư mục output/"""
    os.makedirs("output", exist_ok=True)
    duong_dan = os.path.join("output", ten_file)

    with open(duong_dan, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Status", status])
        writer.writerow([])
        writer.writerow(["Ket qua"])
        if isinstance(ket_qua, list):
            for item in ket_qua:
                writer.writerow([item])
        else:
            writer.writerow([ket_qua])

    return duong_dan