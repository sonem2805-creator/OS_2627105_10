import csv
import time
def doc_file_csv(ten_file, so_tai_nguyen=5):
    pids = []
    allocation = []
    max_demand = []
    available = []
    f = open(ten_file, mode='r', encoding='utf-8')
    reader = csv.reader(f)
    next(reader)
    dong = 0
    for row in reader:
        if len(row) == 0:
            continue
        pids.append(row[0])
        alloc_row = []
        for j in range(1, 1 + so_tai_nguyen):
            alloc_row.append(int(row[j]))
        allocation.append(alloc_row)
        max_row = []
        for j in range(1 + so_tai_nguyen, 1 + 2 * so_tai_nguyen):
            max_row.append(int(row[j]))
        max_demand.append(max_row)
        if dong == 0:
            for j in range(1 + 2 * so_tai_nguyen, 1 + 3 * so_tai_nguyen):
                if row[j] != '':
                    available.append(int(row[j]))
        dong = dong + 1
    f.close()
    return pids, allocation, max_demand, available
def chay_banker(pids, allocation, max_demand, available):
    bat_dau = time.time()
    n = len(pids)
    m = len(available)
    need = []
    for i in range(n):
        hang = []
        for j in range(m):
            hang.append(max_demand[i][j] - allocation[i][j])
        need.append(hang)
    work = []
    for j in range(m):
        work.append(available[j])
    finish = []
    for i in range(n):
        finish.append(False)
    safe_sequence = []
    steps = []
    while len(safe_sequence) < n:
        tim_thay = False
        for i in range(n):
            if finish[i] == False:
                du_tai_nguyen = True
                for j in range(m):
                    if need[i][j] > work[j]:
                        du_tai_nguyen = False
                        break
                if du_tai_nguyen == True:
                    work_truoc = []
                    for j in range(m):
                        work_truoc.append(work[j])
                        work[j] = work[j] + allocation[i][j]
                    work_sau = []
                    for j in range(m):
                        work_sau.append(work[j])
                    finish[i] = True
                    safe_sequence.append(pids[i])
                    tim_thay = True
                    steps.append({
                        "step": len(safe_sequence),
                        "process": pids[i],
                        "need": need[i],
                        "work_before": work_truoc,
                        "allocation": allocation[i],
                        "work_after": work_sau
                    })
        if tim_thay == False:
            break
    ket_thuc = time.time()
    thoi_gian_ms = (ket_thuc - bat_dau) * 1000.0
    an_toan = (len(safe_sequence) == n)
    trang_thai = "UNSAFE"
    if an_toan == True:
        trang_thai = "SAFE"
    chua_xong = []
    for i in range(n):
        if finish[i] == False:
            chua_xong.append(pids[i])
    return {
        "status": trang_thai,
        "is_safe": an_toan,
        "safe_sequence": safe_sequence,
        "unallocated_processes": chua_xong,
        "need_matrix": need,
        "execution_time_ms": round(thoi_gian_ms, 4),
        "steps": steps
    }
if __name__ == "__main__":
    ds_file = [
        "benchmark_50_processes.csv",
        "benchmark_100_processes.csv",
        "benchmark_500_processes.csv"
    ]
    for f in ds_file:
        pids, alloc, max_req, avail = doc_file_csv(f, 5)
        ket_qua = chay_banker(pids, alloc, max_req, avail)
        print(f, "|", ket_qua["status"], "|", ket_qua["execution_time_ms"], "ms | Steps:", len(ket_qua["steps"]))
