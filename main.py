import logging
from pathlib import Path

from duplicate_finder import find_dublicate
from file_identifire import scan_file_signiture
from file_operations import move_file
from folder_selector import select_folder
from logger import setup_log
from organizer import create_organization_plan
from scanner import scan_folder

setup_log()

logger = logging.getLogger(__name__)


def already_scanned(current_folder, scanned_folder):
    if scanned_folder is None:
        return False

    return Path(scanned_folder).resolve() == Path(current_folder).resolve()


def show_menu():
    print("\n==============================")
    print("  INTELLIGENT FILE ORGANIZER")
    print("==============================")
    print("\n1. Select folder")
    print("2. Scan files")
    print("3. Find duplicates")
    print("4. Organize files")
    print("5. View report")
    print("6. Settings")
    print("7. Activity log")
    print("0. Exit")

    while True:
        try:
            choice = int(input("--> "))

            if 0 <= choice <= 7:
                return choice

            print("Invalid! Enter a number between 0 and 7.")

        except ValueError:
            print("Please enter an integer.")


def show_scan_report(scanned_data, identified_file_type):
    print("\n==============================")
    print("        Scanned Report")
    print("==============================")

    for index, file in enumerate(scanned_data, start=1):
        print(f"{index}. {file.name}")

    print(f"\nFiles found: {len(scanned_data)}\n")

    for file_type, files in identified_file_type.items():
        print(f"{file_type} files: {len(files)}")


def show_duplicate_report(duplicate_list, folder_path):
    print("\n==============================")
    print("      Duplicate Report")
    print("==============================")

    for index, duplicate in enumerate(duplicate_list, start=1):
        print(f"{index} :->")

        for i, file in enumerate(duplicate):
            clean_path = file.relative_to(folder_path)
            branch = "└──" if i == len(duplicate) - 1 else "├──"

            print(f"  {branch} {file.name} ({clean_path})")

    print(f"\nDuplicates found: {len(duplicate_list)}")


def show_organization_plan(organization_plan, folder_path):
    print("\n==============================")
    print("       Organization Plan")
    print("==============================")

    for destination, files in organization_plan.items():
        print(f"\n📁 {destination.name}/ {len(files)} files.")

        for i, file in enumerate(files):
            branch = "└──" if i == len(files) - 1 else "├──"
            print(f"\t{branch} {file.relative_to(Path(folder_path))}")


def show_final_report(folder_path, scanned_data, identified_file_type, duplicate_list):
    print("\n==============================")
    print("   File Organization Report")
    print("==============================")

    print(f"Selected Folder: {folder_path}")
    print(f"Total files: {len(scanned_data)}")
    # print(f"Status: {status}")

    print()
    print("File type Breakdown")
    for file_type, files in identified_file_type.items():
        print(f"{file_type} files: {len(files)}")

    print()
    print("Dublicate Information")
    print(f"Duplicate groups: {len(duplicate_list)}")


def main():
    folder_path = None
    scanned_data = None
    identified_file_type = None
    duplicate_list = None
    scanned_folder = None

    while True:
        user_choice = show_menu()

        if user_choice == 0:
            print("Goodbye!")
            break

        # SELECT FOLDER
        elif user_choice == 1:
            selected_path = select_folder()

            if selected_path:
                folder_path = selected_path
                logger.info(f"Selected Folder - {folder_path}")
                scanned_data = None
                identified_file_type = None
                duplicate_list = None
                scanned_folder = None

                print(folder_path)
            else:
                print(f"No folder selected. Current folder: {folder_path}")

        # SCAN FILES
        elif user_choice == 2:
            if not folder_path:
                print("Select a folder before performing any action.")
                continue

            if scanned_data is None or not already_scanned(folder_path, scanned_folder):
                print("Scanning...")
                scanned_data = scan_folder(folder_path)
                scanned_folder = Path(folder_path).resolve()

            if identified_file_type is None:
                print("Identifying file types...")
                identified_file_type = scan_file_signiture(scanned_data)

            show_scan_report(scanned_data, identified_file_type)

        # FIND DUPLICATES
        elif user_choice == 3:
            if not folder_path:
                print("Select a folder before performing any action.")
                continue

            if scanned_data is None or not already_scanned(folder_path, scanned_folder):
                print("Scanning the folder...")
                scanned_data = scan_folder(folder_path)
                scanned_folder = Path(folder_path).resolve()

            if duplicate_list is not None:
                show_duplicate_report(duplicate_list, folder_path)

            else:
                print("Finding duplicates...")
                duplicate_list = find_dublicate(scanned_data)

                show_duplicate_report(duplicate_list, folder_path)

        # ORGANIZE FILES
        elif user_choice == 4:
            if not folder_path:
                print("Select a folder before performing any action.")
                continue

            destination_folder = select_folder()

            if not destination_folder:
                print("No destination folder selected. Try again.")
                continue

            if scanned_data is None or not already_scanned(folder_path, scanned_folder):
                scanned_data = None
                identified_file_type = None

                print("Scanning...")
                scanned_data = scan_folder(folder_path)
                scanned_folder = Path(folder_path).resolve()

            if identified_file_type is None:
                identified_file_type = None
                print("Identifying file types...")
                identified_file_type = scan_file_signiture(scanned_data)

            print("Creating a plan...")

            organization_plan = create_organization_plan(
                identified_file_type, destination_folder
            )

            show_organization_plan(organization_plan, folder_path)

            # CONFIRMATION
            user_conformation = None

            while True:
                try:
                    user_conformation = input("Confirm this plan? (y/n): ")

                    if user_conformation == "y" or user_conformation == "n":
                        break

                except OSError as error:
                    print(f"Invalid input!: {error}")
                    break
            sucessfully_moved = 0
            failed_to_move = 0

            if user_conformation == "y":
                for destination, sources in organization_plan.items():
                    for source in sources:
                        if move_file(source, destination):
                            sucessfully_moved += 1
                            scanned_data = None
                            identified_file_type = None
                            duplicate_list = None
                            scanned_folder = None
                        else:
                            print("Failed to move!")
                            failed_to_move += 1
            else:
                print("User cancelled the plan.")

            print("===============================")
            print("        Moving Report")
            print("===============================")
            print(f"Files successfully moved: {sucessfully_moved}")
            print(f"Files failed to move: {failed_to_move}")

        # OTHER OPTIONS
        elif user_choice == 5:
            if not folder_path:
                print("Select a folder before performing any action.")
                continue

            if (
                scanned_data is None
                or identified_file_type is None
                or not already_scanned(folder_path, scanned_folder)
            ):
                print("Scanning...")
                scanned_data = scan_folder(folder_path)
                scanned_folder = Path(folder_path).resolve()

            if identified_file_type is None:
                print("Identifying file types...")
                identified_file_type = scan_file_signiture(scanned_data)

            if duplicate_list is None:
                print("Finding Duplicates...")
                duplicate_list = find_dublicate(scanned_data)

            show_final_report(
                folder_path, scanned_data, identified_file_type, duplicate_list
            )

        elif user_choice == 6:
            print("Option 6")

        elif user_choice == 7:
            print("Option 7")


if __name__ == "__main__":
    main()
