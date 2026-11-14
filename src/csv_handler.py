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
                    f"Allocation > Max tại {i}"
                )

            row.append(value)

        need.append(row)

    return need


def doc_file_csv(file_path):

    if not os.path.exists(file_path):
        raise CSVValidationError(
            "Không tìm thấy file CSV"
        )

    if os.path.getsize(file_path) == 0:
        raise CSVValidationError(
            "File CSV rỗng"
        )

    allocation = []
    max_need = []
    processes = []
    available = None

    try:

        with open(
            file_path,
            mode="r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                process = row["Process"].strip()

                if process.upper() == "AVAILABLE":

                    available = [
                        int(row["Allocation_A"]),
                        int(row["Allocation_B"]),
                        int(row["Allocation_C"])
                    ]

                    continue

                alloc = [
                    int(row["Allocation_A"]),
                    int(row["Allocation_B"]),
                    int(row["Allocation_C"])
                ]

                max_row = [
                    int(row["Max_A"]),
                    int(row["Max_B"]),
                    int(row["Max_C"])
                ]

                processes.append(process)
                allocation.append(alloc)
                max_need.append(max_row)

    except ValueError:
        raise CSVValidationError(
            "CSV chứa dữ liệu không phải số nguyên"
        )

    if len(processes) == 0:
        raise CSVValidationError(
            "Không có process nào"
        )
    if available is None:
        raise CSVValidationError(
            "Thiếu dòng AVAILABLE"
        )

    need = calculate_need(
        allocation,
        max_need
    )

    return {
        "processes": processes,
        "allocation": allocation,
        "max": max_need,
        "available": available,
        "need": need
    }

import os
import csv

def ghi_file_csv(ten_file, status, ket_qua):
    """
    Ghi kết quả ra thư mục output/
    """

    os.makedirs("output", exist_ok=True)

    duong_dan = os.path.join("output", ten_file)

    with open(
        duong_dan,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

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