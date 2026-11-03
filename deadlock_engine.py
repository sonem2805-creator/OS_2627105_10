"""
deadlock_engine.py
Mo phong thuat toan phat hien Deadlock:
- Deadlock Detection
- Luu lich su ma tran qua tung buoc
- Tra ve du lieu chuan hoa cho giao dien
"""

from copy import deepcopy


def _validate_state(allocation, request, available):
    """Kiem tra tinh hop le cua du lieu dau vao."""

    if len(allocation) == 0:
        raise ValueError("Phai co it nhat mot tien trinh.")

    if len(request) != len(allocation):
        raise ValueError(
            "Request phai co cung so tien trinh voi Allocation."
        )

    if len(available) == 0:
        raise ValueError("Phai co it nhat mot loai tai nguyen.")

    resource_count = len(available)

    for i in range(len(allocation)):

        if len(allocation[i]) != resource_count:
            raise ValueError("Allocation co so cot khong hop le.")

        if len(request[i]) != resource_count:
            raise ValueError("Request co so cot khong hop le.")

        for j in range(resource_count):

            if not isinstance(allocation[i][j], int) or isinstance(allocation[i][j], bool):
                raise ValueError("Allocation phai gom so nguyen.")

            if not isinstance(request[i][j], int) or isinstance(request[i][j], bool):
                raise ValueError("Request phai gom so nguyen.")

            if allocation[i][j] < 0 or request[i][j] < 0:
                raise ValueError(
                    "So luong tai nguyen khong duoc am."
                )

    for value in available:

        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("Available phai gom so nguyen.")

        if value < 0:
            raise ValueError("Available khong duoc am.")


def detect_deadlock(allocation, request, available):
    """
    Phat hien Deadlock trong he thong.

    Tra ve dict gom:
        status: SAFE hoac DEADLOCK
        safe_sequence: Chuoi tien trinh hoan thanh
        deadlocked_pids: Danh sach tien trinh bi ket
        history: Lich su ma tran qua tung buoc
    """

    _validate_state(allocation, request, available)

    process_count = len(allocation)
    resource_count = len(available)

    # Khoi tao Work
    work = available.copy()

    # Khoi tao Finish
    finish = [
        all(resource == 0 for resource in allocation[i])
        for i in range(process_count)
    ]

    safe_sequence = []
    history = []

    # Ham luu lich su tung buoc
    def save_history(step, process, status):
        history.append({
            "step": step,
            "process": process,
            "allocation": deepcopy(allocation),
            "request": deepcopy(request),
            "work": work.copy(),
            "finish": finish.copy(),
            "status": status
        })

    # Luu trang thai ban dau
    save_history(
        step=0,
        process=None,
        status="INITIAL"
    )

    # Tim tien trinh co the hoan thanh
    while True:

        found_process = False

        for i in range(process_count):

            if finish[i]:
                continue

            # Kiem tra Request[i] <= Work
            can_finish = all(
                request[i][j] <= work[j]
                for j in range(resource_count)
            )

            if can_finish:

                # Tien trinh hoan thanh va tra tai nguyen
                for j in range(resource_count):
                    work[j] += allocation[i][j]

                finish[i] = True
                safe_sequence.append(f"P{i}")
                found_process = True

                # Luu lich su buoc an toan
                save_history(
                    step=len(safe_sequence),
                    process=f"P{i}",
                    status="SAFE"
                )

        if not found_process:
            break

    # Xac dinh cac tien trinh bi Deadlock
    deadlocked_pids = [
        f"P{i}"
        for i in range(process_count)
        if not finish[i]
    ]

    if deadlocked_pids:

        status = "DEADLOCK"

        # Luu buoc phat hien Deadlock
        save_history(
            step=len(safe_sequence) + 1,
            process=None,
            status="DEADLOCK"
        )

    else:

        status = "SAFE"

    # Tra ve ket qua chuan hoa
    return {
        "status": status,
        "safe_sequence": safe_sequence,
        "deadlocked_pids": deadlocked_pids,
        "history": history
    }


if __name__ == "__main__":

    # Du lieu mau kiem tra Deadlock
    allocation = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

    request = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0]
    ]

    available = [0, 0, 0]

    print("===== DEADLOCK DETECTION =====")

    result = detect_deadlock(
        allocation,
        request,
        available
    )

    print("Status:", result["status"])
    print("Safe Sequence:", result["safe_sequence"])
    print("Deadlocked PIDs:", result["deadlocked_pids"])

    print("\n===== HISTORY =====")

    for step in result["history"]:
        print(step)