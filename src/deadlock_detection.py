allocation = [
    [0, 1],
    [2, 0],
    [1, 1]
]
request = [
    [1, 0],
    [0, 1],
    [1, 1]
]
available = [0, 0]
num_process = len(allocation)
num_resource = len(available)
work = available.copy()
finish = [False] * num_process
for i in range(num_process):
    empty = True
    for j in range(num_resource):
        if allocation[i][j] != 0:
            empty = False
    if empty:
        finish[i] = True
changed = True
while changed:
    changed = False
    for i in range(num_process):
        if finish[i]:
            continue
        can_finish = True
        for j in range(num_resource):
            if request[i][j] > work[j]:
                can_finish = False
                break
        if can_finish:
            for j in range(num_resource):
                work[j] += allocation[i][j]
            finish[i] = True
            changed = True
deadlocked = []
for i in range(num_process):
    if not finish[i]:
        deadlocked.append(f"P{i}")
if len(deadlocked) == 0:
    print("No Deadlock")
else:
    print("Deadlocked Processes:")
    print(", ".join(deadlocked))