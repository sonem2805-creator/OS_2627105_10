# Banker's Algorithm

allocation = [
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2]
]

max_need = [
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2],
    [2, 2, 2],
    [4, 3, 3]
]

available = [3, 3, 2]

num_process = len(allocation)
num_resource = len(available)

# Tính Need
need = []

for i in range(num_process):
    row = []
    for j in range(num_resource):
        row.append(max_need[i][j] - allocation[i][j])
    need.append(row)

work = available.copy()
finish = [False] * num_process
safe_sequence = []

while len(safe_sequence) < num_process:

    found = False

    for i in range(num_process):

        if finish[i]:
            continue

        can_run = True

        for j in range(num_resource):
            if need[i][j] > work[j]:
                can_run = False
                break

        if can_run:

            for j in range(num_resource):
                work[j] += allocation[i][j]

            finish[i] = True
            safe_sequence.append(i)
            found = True

    if not found:
        break

if len(safe_sequence) == num_process:
    print("SAFE STATE")
    print("Safe Sequence:")

    for p in safe_sequence:
        print(f"P{p}", end=" ")

else:
    print("UNSAFE STATE")