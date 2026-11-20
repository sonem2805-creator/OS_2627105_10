"""
main.py
Chuong trinh mo phong (Console CLI):
- Banker Safety Check
- Banker Resource Request
- Deadlock Detection & Recovery
- Doc du lieu CSV tu input/ va xuat ket qua ra output/
"""
import os
from source.banker_engine import chay_banker, resource_request
from source.deadlock_engine import detect_deadlock
from source.csv_handler import doc_file_csv, ghi_file_csv, CSVValidationError


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
    """Chay Banker Safety Check (Du lieu mau)."""
    print("\n=== THUAT TOAN BANKER ===")
    allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    maximum = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    available = [3, 3, 2]
    pids = ["P0", "P1", "P2", "P3", "P4"]

    result = chay_banker(pids, allocation, maximum, available)
    print("Status:", result["status"])
    print("Execution Time (ms):", result["execution_time_ms"])
    print("Safe Sequence:", result["safe_sequence"])
    print("Deadlocked PIDs:", result["deadlocked_pids"])

    out_path = ghi_file_csv("banker_result.csv", result["status"], result["safe_sequence"])
    print(f"Da luu ket qua vao: {out_path}")
    return result


def banker_request_demo():
    """Mo phong yeu cau cap phat tai nguyen."""
    print("\n=== BANKER RESOURCE REQUEST ===")
    allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    maximum = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
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
    print("Available:", result["available"])
    return result


def show_deadlock(result):
    """Hien thi ket qua phat hien Deadlock."""
    print("Status:", result["status"])
    print("Deadlocked PIDs:", result["deadlocked_pids"])
    if result["deadlocked_pids"]:
        print("Phat hien Deadlock tai:", ", ".join(result["deadlocked_pids"]))
    else:
        print("Khong phat hien Deadlock.")


def deadlock_demo(recover=False):
    """Mo phong phat hien va phuc hoi Deadlock."""
    print("\n=== PHAT HIEN DEADLOCK ===")
    allocation = [[1, 0], [0, 1]]
    request = [[0, 1], [1, 0]]
    available = [0, 0]

    if not recover:
        request[0] = [0, 0]

    result = detect_deadlock(allocation, request, available)
    show_deadlock(result)

    if not recover or not result["deadlocked_pids"]:
        return result

    print("\n=== PHUC HOI DEADLOCK ===")
    victim_pid = result["deadlocked_pids"][0]
    victim_index = int(victim_pid[1:])
    print(f"Ket thuc tien trinh {victim_pid}")

    for j in range(len(available)):
        available[j] += allocation[victim_index][j]
        allocation[victim_index][j] = 0
        request[victim_index][j] = 0

    print("Available sau phuc hoi:", available)
    recovery_result = detect_deadlock(allocation, request, available)
    print("\n=== KIEM TRA SAU PHUC HOI ===")
    show_deadlock(recovery_result)
    return recovery_result


def run_from_csv():
    """Chay mo phong tu file CSV bat ky trong thu muc input/."""
    path = input("Nhap duong dan file CSV (VD: input/oracle/oracle_1_safe.csv): ").strip()
    try:
        data = doc_file_csv(path)
        print(f"\n[OK] Nap thanh cong {len(data['processes'])} tien trinh, {len(data['available'])} tai nguyen.")
        res = chay_banker(data["processes"], data["allocation"], data["max"], data["available"])
        print("Status:", res["status"])
        print("Thoi gian chay (ms):", res["execution_time_ms"])
        print("Chuoi an toan:", res["safe_sequence"])
        out_path = ghi_file_csv("csv_run_result.csv", res["status"], res["safe_sequence"])
        print(f"Da xuat ket qua ra: {out_path}")
    except CSVValidationError as e:
        print(f"[LOI DU LIEU CSV]: {e}")
    except Exception as e:
        print(f"[LOI HE THONG]: {e}")


def main():
    """Menu chinh cua chuong trinh."""
    while True:
        print("\n================================")
        print(" MO PHONG BANKER VA DEADLOCK")
        print("================================")
        print("1. Chay thuat toan Banker (Du lieu mau)")
        print("2. Banker Resource Request")
        print("3. Phat hien Deadlock (khong co)")
        print("4. Phat hien va phuc hoi Deadlock")
        print("5. Nap file CSV tu input/ va chay Banker")
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
        elif choice == "5":
            run_from_csv()
        elif choice == "0":
            print("Ket thuc chuong trinh.")
            break
        else:
            print("Lua chon khong hop le!")


if __name__ == "__main__":
    main()