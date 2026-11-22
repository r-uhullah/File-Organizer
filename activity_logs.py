from collections import deque


def show_activity_log():
    print("\n==============================")
    print("         ACTIVITY LOGS")
    print("==============================")
    print("\n1. View recent activity")
    print("2. View errors and warnings")
    print("3. View organization history")
    print("4. View scan history")
    print("5. Open log file")
    print("0. Back to main menu")

    while True:
        try:
            user_choice = int(input("-->  "))

            if 0 <= user_choice <= 5:
                break

            print("Enter an integer between (0-5)")

        except ValueError:
            print("Invalid! Enter an integer (0-5)")

    return user_choice


def read_full_log(log_file="organizer.log"):
    try:
        with open(log_file, "r", encoding="utf-8") as file:
            log_data = file.readlines()

        return log_data
    except FileNotFoundError:
        print(f"Log file '{log_file}' does not exists yet.")
        return None


def view_recent_activity(log_file="organizer.log", num_lines=10):
    print("\n==============================")
    print("         RECENT ACTIVITY")
    print("==============================")

    try:
        with open(log_file, "r", encoding="utf-8") as file:
            latest_lines = deque(file, maxlen=num_lines)

        print(f"Showing Latest {len(latest_lines)} Logs.")
        print()
        for index, line in enumerate(latest_lines, start=1):
            print(f"{index}. {line.strip()}")

    except FileNotFoundError:
        print(f"Log file '{log_file}' does not exist yet.")


def view_errors_and_warnings(full_log_data, log_flie="organizer.log"):
    if full_log_data is None:
        print("No log data to read.")
        return False

    print("\n==============================")
    print("       ERRORS & WARNINGS")
    print("==============================")

    warning = 0
    error = 0
    critical = 0

    for index, line in enumerate(full_log_data, start=1):
        if " - ERROR - " in line:
            print(f"{index}. {line.strip()}")
            error += 1

        if " - WARNING - " in line:
            print(f"{index}. {line.strip()}")
            warning += 1

        if " - CRITICAL - " in line:
            print(f"{index}. {line.strip()}")
            critical += 1

    print(f"Warnings: {warning}")
    print(f"Errors: {error}")
    print(f"Criticals: {critical}")


def view_organization_history(full_log_data, log_file="organizer.log"):
    print("\n==============================")
    print("       View Organization History")
    print("==============================")

    for index, line in enumerate(full_log_data, start=1):
        print(f"Operation #{index}")

        if "source" in line and "destination" in line:
            print(line)
