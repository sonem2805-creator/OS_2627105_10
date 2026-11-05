"""
banker_engine.py
Mo phong thuat toan Banker:
- Safety Check
- Resource Request
- Luu lich su ma tran qua tung buoc
"""

from copy import deepcopy


def _validate_state(allocation, maximum, available):
    """Kiem tra tinh hop le cua du lieu dau vao."""

    if len(allocation) == 0:
        raise ValueError("Phai co it nhat mot tien trinh.")

    if len(allocation) != len(maximum):
        raise ValueError(
            "Allocation va Maximum phai co cung so tien trinh."
        )

    if len(available) == 0:
        raise ValueError("Phai co it nhat mot loai tai nguyen.")

    resource_count = len(available)

    for i in range(len(allocation)):
        if len(allocation[i]) != resource_count:
            raise ValueError("Allocation co so cot khong hop le.")

        if len(maximum[i]) != resource_count:
            raise ValueError("Maximum co so cot khong hop le.")

        for j in range(resource_count):
            if not isinstance(allocation[i][j], int) or isinstance(allocation[i][j], bool):
                raise ValueError("Allocation phai gom so nguyen.")

            if not isinstance(maximum[i][j], int) or isinstance(maximum[i][j], bool):
                raise ValueError("Maximum phai gom so nguyen.")

            if allocation[i][j] < 0 or maximum[i][j] < 0:
                raise ValueError("So luong tai nguyen khong duoc am.")

            if allocation[i][j] > maximum[i][j]:
                raise ValueError(
                    f"Allocation vuot Maximum tai tien trinh P{i}."
                )

    for value in available:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("Available phai gom so nguyen.")

        if value < 0:
            raise ValueError("Available khong duoc am.")


def safety_check(allocation, maximum, available):
    """
    Kiem tra trang thai an toan.

    Tra ve dict:
        status: SAFE hoac DEADLOCK
        safe_sequence: Chuoi an toan
        deadlocked_pids: Cac tien trinh chua hoan thanh
        history: Lich su ma tran tung buoc
    """

    _validate_state(allocation, maximum, available)

    process_count = len(allocation)
    resource_count = len(available)

    # Tinh Need = Maximum - Allocation
    need = [
        [
            maximum[i][j] - allocation[i][j]
            for j in range(resource_count)
        ]
        for i in range(process_count)
    ]

    work = available.copy()
    finish = [False] * process_count

    safe_sequence = []
    history = []

    while True:
        found_process = False

        for i in range(process_count):

            if finish[i]:
                continue

            # Kiem tra Need[i] <= Work
            can_finish = all(
                need[i][j] <= work[j]
                for j in range(resource_count)
            )

            if can_finish:

                # Gia su tien trinh hoan thanh
                # va tra lai tai nguyen
                for j in range(resource_count):
                    work[j] += allocation[i][j]

                finish[i] = True
                safe_sequence.append(f"P{i}")
                found_process = True

                # Luu lich su tung buoc
                history.append({
                    "step": len(history) + 1,
                    "process": f"P{i}",
                    "allocation": deepcopy(allocation),
                    "need": deepcopy(need),
                    "work": work.copy(),
                    "finish": finish.copy(),
                    "status": "SAFE"
                })

        if not found_process:
            break

    # Tim cac tien trinh chua hoan thanh
    deadlocked_pids = [
        f"P{i}"
        for i in range(process_count)
        if not finish[i]
    ]

    if deadlocked_pids:

        status = "DEADLOCK"
        safe_sequence = []

        history.append({
            "step": len(history) + 1,
            "process": None,
            "allocation": deepcopy(allocation),
            "need": deepcopy(need),
            "work": work.copy(),
            "finish": finish.copy(),
            "status": "DEADLOCK"
        })

    else:
        status = "SAFE"

    return {
        "status": status,
        "safe_sequence": safe_sequence,
        "deadlocked_pids": deadlocked_pids,
        "history": history
    }


def resource_request(
    process_id, request, allocation, maximum, available
):
    """
    Xu ly yeu cau tai nguyen theo Banker.

    Tra ve dict:
        status: GRANTED, WAIT, DENIED_UNSAFE, ERROR_NEED
        safety_status: SAFE, DEADLOCK hoac None
        safe_sequence
        deadlocked_pids
        history
        allocation
        available
        message
    """

    _validate_state(allocation, maximum, available)

    process_count = len(allocation)
    resource_count = len(available)

    if not isinstance(process_id, int) or isinstance(process_id, bool):
        raise ValueError("process_id phai la so nguyen.")

    if not 0 <= process_id < process_count:
        raise ValueError("process_id khong hop le.")

    if len(request) != resource_count:
        raise ValueError("Request phai co dung so loai tai nguyen.")

    for value in request:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("Request phai gom so nguyen.")

        if value < 0:
            raise ValueError("Request khong duoc am.")

    # Tinh Need
    need = [
        [
            maximum[i][j] - allocation[i][j]
            for j in range(resource_count)
        ]
        for i in range(process_count)
    ]

    # Buoc 1: Kiem tra Request <= Need
    if any(
        request[j] > need[process_id][j]
        for j in range(resource_count)
    ):
        return {
            "status": "ERROR_NEED",
            "safety_status": None,
            "safe_sequence": [],
            "deadlocked_pids": [],
            "history": [],
            "allocation": deepcopy(allocation),
            "available": available.copy(),
            "message": "Yeu cau vuot qua nhu cau toi da con lai."
        }

    # Buoc 2: Kiem tra Request <= Available
    if any(
        request[j] > available[j]
        for j in range(resource_count)
    ):
        return {
            "status": "WAIT",
            "safety_status": None,
            "safe_sequence": [],
            "deadlocked_pids": [],
            "history": [],
            "allocation": deepcopy(allocation),
            "available": available.copy(),
            "message": "Chua du tai nguyen; yeu cau phai cho."
        }

    # Buoc 3: Cap phat thu tren ban sao
    new_allocation = deepcopy(allocation)
    new_available = available.copy()

    for j in range(resource_count):
        new_available[j] -= request[j]
        new_allocation[process_id][j] += request[j]

    # Buoc 4: Kiem tra an toan sau cap phat
    safety_result = safety_check(
        new_allocation,
        maximum,
        new_available
    )

    if safety_result["status"] == "SAFE":

        return {
            "status": "GRANTED",
            "safety_status": "SAFE",
            "safe_sequence": safety_result["safe_sequence"],
            "deadlocked_pids": [],
            "history": safety_result["history"],
            "allocation": new_allocation,
            "available": new_available,
            "message": "Chap nhan cap phat; he thong van an toan."
        }

    # Tu choi cap phat neu he thong khong an toan
    return {
        "status": "DENIED_UNSAFE",
        "safety_status": "DEADLOCK",
        "safe_sequence": [],
        "deadlocked_pids": safety_result["deadlocked_pids"],
        "history": safety_result["history"],
        "allocation": deepcopy(allocation),
        "available": available.copy(),
        "message": "Tu choi cap phat vi he thong se khong an toan."
    }


if __name__== "__main__":

    # Du lieu mau Banker
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    maximum = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    available = [3, 3, 2]

    print("===== BANKER SAFETY CHECK =====")

    result = safety_check(
        allocation,
        maximum,
        available
    )

    print("Status:", result["status"])
    print("Safe Sequence:", result["safe_sequence"])
    print("Deadlocked PIDs:", result["deadlocked_pids"])

    print("\n===== HISTORY =====")

    for step in result["history"]:
        print(step)

    print("\n===== RESOURCE REQUEST =====")

    request_result = resource_request(
        process_id=1,
        request=[1, 0, 2],
        allocation=allocation,
        maximum=maximum,
        available=available
    )

    print("Status:", request_result["status"])
    print("Safety Status:", request_result["safety_status"])
    print("Message:", request_result["message"])
    print("Safe Sequence:", request_result["safe_sequence"])
    print("Available:", request_result["available"])