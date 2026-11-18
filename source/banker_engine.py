import csv
import time
import os


def doc_file_csv(ten_file, so_tai_nguyen=5):
    pids = []
    allocation = []
    max_demand = []
    available = []
    with open(ten_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        dong = 0
        for row in reader:
            if len(row) == 0:
                continue
            pids.append(row[0])
            alloc_row = [int(row[j]) for j in range(1, 1 + so_tai_nguyen)]
            allocation.append(alloc_row)
            max_row = [int(row[j]) for j in range(1 + so_tai_nguyen, 1 + 2 * so_tai_nguyen)]
            max_demand.append(max_row)
            if dong == 0:
                for j in range(1 + 2 * so_tai_nguyen, 1 + 3 * so_tai_nguyen):
                    if j < len(row) and row[j] != '':
                        available.append(int(row[j]))
            dong += 1
    return pids, allocation, max_demand, available


def chay_banker(pids, allocation, max_demand, available):
    bat_dau = time.time()
    n = len(pids)
    m = len(available)
    need = [[max_demand[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
    work = list(available)
    finish = [False] * n
    safe_sequence = []
    steps = []

    while len(safe_sequence) < n:
        tim_thay = False
        for i in range(n):
            if not finish[i]:
                if all(need[i][j] <= work[j] for j in range(m)):
                    work_truoc = list(work)
                    for j in range(m):
                        work[j] += allocation[i][j]
                    work_sau = list(work)
                    finish[i] = True
                    safe_sequence.append(pids[i])
                    tim_thay = True
                    steps.append({
                        "step": len(safe_sequence),
                        "process": pids[i],
                        "status": "FINISHED",
                        "need": need[i],
                        "work_before": work_truoc,
                        "work": work_sau,
                        "allocation": allocation[i],
                        "work_after": work_sau,
                        "finish": list(finish)
                    })
        if not tim_thay:
            break

    ket_thuc = time.time()
    thoi_gian_ms = (ket_thuc - bat_dau) * 1000.0
    an_toan = (len(safe_sequence) == n)
    trang_thai = "SAFE" if an_toan else "UNSAFE"
    chua_xong = [pids[i] for i in range(n) if not finish[i]]

    return {
        "status": trang_thai,
        "is_safe": an_toan,
        "safe_sequence": safe_sequence,
        "unallocated_processes": chua_xong,
        "deadlocked_pids": chua_xong,
        "need_matrix": need,
        "execution_time_ms": round(thoi_gian_ms, 4),
        "steps": steps,
        "history": steps
    }


def safety_check(allocation, maximum, available):
    """Ham chuan hoa ket noi voi main.py."""
    pids = [f"P{i}" for i in range(len(allocation))]
    return chay_banker(pids, allocation, maximum, available)


def resource_request(process_id, request, allocation, maximum, available):
    """Mo phong yeu cau cap phat tai nguyen (Resource Request)."""
    n = len(allocation)
    m = len(available)
    need = [[maximum[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]

    # 1. Kiem tra Request <= Need
    if any(request[j] > need[process_id][j] for j in range(m)):
        return {
            "status": "REJECTED",
            "safety_status": "UNSAFE",
            "message": f"Loi: P{process_id} yeu cau vuot qua nhu cau toi da (Need).",
            "safe_sequence": [],
            "deadlocked_pids": [],
            "available": available,
            "history": []
        }

    # 2. Kiem tra Request <= Available
    if any(request[j] > available[j] for j in range(m)):
        return {
            "status": "WAIT",
            "safety_status": "UNSAFE",
            "message": f"P{process_id} phai cho do tai nguyen kha dung (Available) khong du.",
            "safe_sequence": [],
            "deadlocked_pids": [],
            "available": available,
            "history": []
        }

    # 3. Gia su cap phat thu
    new_available = [available[j] - request[j] for j in range(m)]
    new_allocation = [list(row) for row in allocation]
    for j in range(m):
        new_allocation[process_id][j] += request[j]

    check = safety_check(new_allocation, maximum, new_available)
    if check["status"] == "SAFE":
        return {
            "status": "GRANTED",
            "safety_status": "SAFE",
            "message": f"Chap nhan cap phat cho P{process_id}. He thong van AN TOAN.",
            "safe_sequence": check["safe_sequence"],
            "deadlocked_pids": [],
            "available": new_available,
            "history": check["history"]
        }
    else:
        return {
            "status": "DENIED",
            "safety_status": "UNSAFE",
            "message": f"Tu choi cap phat cho P{process_id} vi gay mat an toan (UNSAFE).",
            "safe_sequence": [],
            "deadlocked_pids": check["deadlocked_pids"],
            "available": available,
            "history": check["history"]
        }


if __name__ == "__main__":
    ds_file = [
        os.path.join("input", "benchmark_50_processes.csv"),
        os.path.join("input", "benchmark_100_processes.csv"),
        os.path.join("input", "benchmark_500_processes.csv")
    ]
    for f in ds_file:
        if os.path.exists(f):
            pids, alloc, max_req, avail = doc_file_csv(f, 5)
            ket_qua = chay_banker(pids, alloc, max_req, avail)
            print(f, "|", ket_qua["status"], "|", ket_qua["execution_time_ms"], "ms | Steps:", len(ket_qua["steps"]))