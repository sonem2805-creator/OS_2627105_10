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

    allocation = []
    max_need = []
    processes = []
    available = None

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

            allocation.append([
                int(row["Allocation_A"]),
                int(row["Allocation_B"]),
                int(row["Allocation_C"])
            ])

            max_need.append([
                int(row["Max_A"]),
                int(row["Max_B"]),
                int(row["Max_C"])
            ])

            processes.append(process)

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