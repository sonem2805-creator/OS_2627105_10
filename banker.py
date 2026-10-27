import csv
def doc_file_csv(duong_dan):
    pids = []
    allocation = []
    max_need = []
    available = []
    with open(duong_dan, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for dong in reader:
            if len(dong) < 7:
                continue
            pids.append(dong[0].strip())
            alloc_row = [int(dong[1]), int(dong[2]), int(dong[3])]
            max_row = [int(dong[4]), int(dong[5]), int(dong[6])]
            allocation.append(alloc_row)
            max_need.append(max_row)
            if len(available) == 0 and len(dong) >= 10:
                if dong[7].strip() != "":
                    available = [int(dong[7]), int(dong[8]), int(dong[9])]
    return pids, allocation, max_need, available
def tinh_need(allocation, max_need):
    need = []
    n = len(allocation)
    m = len(allocation[0])
    for i in range(n):
        dong = []
        for j in range(m):
            dong.append(max_need[i][j] - allocation[i][j])
        need.append(dong)
    return need
def kiem_tra_an_toan(pids, allocation, need, available):
    n = len(pids)
    m = len(available)
    work = []
    for j in range(m):
        work.append(available[j])
    finish = [False] * n
    chuoi_an_toan = []
    lich_su_work = []
    while len(chuoi_an_toan) < n:
        tim_thay = False
        for i in range(n):
            if not finish[i]:
                du_tai_nguyen = True
                for j in range(m):
                    if need[i][j] > work[j]:
                        du_tai_nguyen = False
                        break
                if du_tai_nguyen:
                    for j in range(m):
                        work[j] = work[j] + allocation[i][j]
                    finish[i] = True
                    chuoi_an_toan.append(pids[i])
                    lich_su_work.append([work[0], work[1], work[2]])
                    tim_thay = True
        if not tim_thay:
            break
    ds_deadlock = []
    for i in range(n):
        if not finish[i]:
            ds_deadlock.append(pids[i])
    an_toan = (len(chuoi_an_toan) == n)
    return an_toan, chuoi_an_toan, ds_deadlock, lich_su_work
def ghi_file_csv(duong_dan, pids, allocation, max_need, need, an_toan, chuoi_an_toan, ds_deadlock):
    with open(duong_dan, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "pid", "alloc_A", "alloc_B", "alloc_C",
            "max_A", "max_B", "max_C",
            "need_A", "need_B", "need_C"
        ])
        for i in range(len(pids)):
            writer.writerow([
                pids[i],
                allocation[i][0], allocation[i][1], allocation[i][2],
                max_need[i][0], max_need[i][1], max_need[i][2],
                need[i][0], need[i][1], need[i][2]
            ])
        writer.writerow([])
        writer.writerow(["Trang thai", "SAFE" if an_toan else "UNSAFE / DEADLOCK"])
        writer.writerow(["Safe Sequence", " -> ".join(chuoi_an_toan)])
        writer.writerow(["Deadlock Processes", ", ".join(ds_deadlock)])
