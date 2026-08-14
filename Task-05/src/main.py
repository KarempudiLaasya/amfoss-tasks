import os
import time


def get_process_cpu(pid):
    try:
        with open(f"/proc/{pid}/stat", "r") as file:
            data = file.read().split()

        return int(data[13]) + int(data[14])
    except (FileNotFoundError, PermissionError):
        return None


def get_total_cpu():
    with open("/proc/stat", "r") as file:
        line = file.readline().split()

    return sum(map(int, line[1:]))


def get_process_info():
    processes = []

    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue

        try:
            with open(f"/proc/{pid}/comm", "r") as file:
                name = file.read().strip()

            with open(f"/proc/{pid}/status", "r") as file:
                memory = 0

                for line in file:
                    if line.startswith("VmRSS:"):
                        memory = int(line.split()[1])
                        break

            cpu = get_process_cpu(pid)

            if cpu is not None:
                processes.append((int(pid), name, cpu, memory))

        except (FileNotFoundError, PermissionError):
            pass

    return processes


previous_process_cpu = {}
previous_total_cpu = get_total_cpu()

while True:
    time.sleep(0.5)

    current_total_cpu = get_total_cpu()
    total_diff = current_total_cpu - previous_total_cpu

    processes = get_process_info()

    os.system("clear")

    print("=" * 70)
    print("                 GRAND LINE GUARDIAN")
    print("=" * 70)
    print(f"Total Active Processes: {len(processes)}")
    print()
    print(f"{'PID':<8}{'PROCESS NAME':<25}{'CPU %':<12}{'MEMORY (KB)':<15}")
    print("-" * 70)

    for pid, name, cpu_time, memory in processes:
        old_cpu = previous_process_cpu.get(pid)

        if old_cpu is not None and total_diff > 0:
            cpu_percent = ((cpu_time - old_cpu) / total_diff) * 100
        else:
            cpu_percent = 0.0

        print(f"{pid:<8}{name[:24]:<25}{cpu_percent:<12.2f}{memory:<15}")

    previous_process_cpu = {
        pid: cpu_time for pid, name, cpu_time, memory in processes
    }

    previous_total_cpu = current_total_cpu
