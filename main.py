"""
main.py
Chuong trinh mo phong:
- Banker Safety Check
- Banker Resource Request
- Deadlock Detection
- Deadlock Recovery
"""

from banker_engine import safety_check, resource_request
from deadlock_engine import detect_deadlock


def print_history(history):
    """Hien thi lich su tung buoc."""

    for step in history:
        print(
            f"Step {step['step']} | "
            f"Process: {step['process']} | "
            f"Status: {step['status']}"
        )
        print("Work:", step["work"])

        if "allocation" in step:
            print("Allocation:", step["allocation"])

        if "need" in step:
            print("Need:", step["need"])

        if "request" in step:
            print("Request:", step["request"])

        print("Finish:", step["finish"])
        print("-" * 50)


def banker():
    """Chay Banker Safety Check."""

    print("\n=== THUAT TOAN BANKER ===")

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

    result = safety_check(
        allocation,
        maximum,
        available
    )

    print("Status:", result["status"])
    print("Safe Sequence:", result["safe_sequence"])
    print("Deadlocked PIDs:", result["deadlocked_pids"])

    print("\n=== BANKER HISTORY ===")
    print_history(result["history"])

    return result


def banker_request_demo():
    """Mo phong yeu cau cap phat tai nguyen."""

    print("\n=== BANKER RESOURCE REQUEST ===")

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

    result = resource_request(
        process_id=1,
        request=[1, 0, 2],
        allocation=allocation,
        maximum=maximum,
        available=available
    )

    print("Status:", result["status"])
    print("Safety Status:", result["safety_status"])
    print("Message:", result["message"])
    print("Safe Sequence:", result["safe_sequence"])
    print("Deadlocked PIDs:", result["deadlocked_pids"])
    print("Available:", result["available"])

    print("\n=== REQUEST HISTORY ===")
    print_history(result["history"])

    return result


def show_deadlock(result):
    """Hien thi ket qua phat hien Deadlock."""

    print("Status:", result["status"])
    print("Safe Sequence:", result["safe_sequence"])
    print("Deadlocked PIDs:", result["deadlocked_pids"])

    if result["deadlocked_pids"]:
        print(
            "Phat hien Deadlock tai:",
            ", ".join(result["deadlocked_pids"])
        )
    else:
        print("Khong phat hien Deadlock.")


def deadlock_demo(recover=False):
    """Mo phong phat hien va phuc hoi Deadlock."""

    print("\n=== PHAT HIEN DEADLOCK ===")

    allocation = [
        [1, 0],
        [0, 1]
    ]

    request = [
        [0, 1],
        [1, 0]
    ]

    available = [0, 0]

    # Neu khong phuc hoi, tao tinh huong an toan
    if not recover:
        request[0] = [0, 0]

    result = detect_deadlock(
        allocation,
        request,
        available
    )

    show_deadlock(result)

    print("\n=== DEADLOCK HISTORY ===")
    print_history(result["history"])

    if not recover or not result["deadlocked_pids"]:
        return result

    # Phuc hoi bang cach ket thuc mot tien trinh bi ket
    print("\n=== PHUC HOI DEADLOCK ===")

    victim_pid = result["deadlocked_pids"][0]
    victim_index = int(victim_pid[1:])

    print(f"Ket thuc tien trinh {victim_pid}")

    # Thu hoi tai nguyen cua tien trinh bi ket
    for j in range(len(available)):
        available[j] += allocation[victim_index][j]

        allocation[victim_index][j] = 0
        request[victim_index][j] = 0

    print("Available sau phuc hoi:", available)

    # Kiem tra lai sau khi phuc hoi
    recovery_result = detect_deadlock(
        allocation,
        request,
        available
    )

    print("\n=== KIEM TRA SAU PHUC HOI ===")
    show_deadlock(recovery_result)

    if recovery_result["status"] == "SAFE":
        print("Phuc hoi thanh cong trong mo phong.")

    print("\n=== RECOVERY HISTORY ===")
    print_history(recovery_result["history"])

    return recovery_result


def main():
    """Menu chinh cua chuong trinh."""

    while True:

        print("\n================================")
        print(" MO PHONG BANKER VA DEADLOCK")
        print("================================")
        print("1. Chay thuat toan Banker")
        print("2. Banker Resource Request")
        print("3. Phat hien Deadlock (khong co)")
        print("4. Phat hien va phuc hoi Deadlock")
        print("0. Thoat")

        choice = input("Nhap lua chon: ").strip()

        if choice == "1":
            banker()

        elif choice == "2":
            banker_request_demo()

        elif choice == "3":
            deadlock_demo(False)

        elif choice == "4":
            deadlock_demo(True)

        elif choice == "0":
            print("Ket thuc chuong trinh.")
            break

        else:
            print("Lua chon khong hop le!")


if __name__ == "__main__":
    main()