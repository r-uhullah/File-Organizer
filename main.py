from pathlib import Path

from duplicate_finder import find_dublicate  # to scan for dublicate files
from file_identifire import (
    scan_file_signiture,  # to scan for the file extention using signiture
)
from folder_selector import select_folder  # to show the folder selection window
from organizer import (
    create_organization_plan,  # to compare the files with the identifies_file_type and create a plan to seprate it into different folders
)
from scanner import (
    scan_folder,  # to scan the selected folder and get a list of all the files in it
)


# to check if the current path of selected folder has already been scanned
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

    # Continueing to ask for an input until a valid option is not received
    while True:
        # to catch if the user enters anything else than an integer
        try:
            user_choice = int(input("-->  "))
            # to make keep asking for an input until the user enters a valid integer in range
            if (user_choice < 0) or (user_choice > 7):
                print("Invalid!! Try again between (0-7).")
            else:
                break
        except ValueError:
            print("Enter an Integer between (0-7)")

    return user_choice  # returning the value of the user_choice to use in the main function


def main():
    folder_path = None  # to store the path of the selected folder
    identified_file_type = (
        {}
    )  # stores the list of file types from the scan_file_signiture function
    scanned_data = (
        None  # saving the data that comes from the scanner function (for optimization)
    )
    scanned_folder = None  # to check if the user has already scanned the folder he is trying to if yes then scanned_data is used insted of scanning (for optimization)

    # keeps showing the menu until the user exits the program
    while True:
        user_choice = show_menu()

        # to exit if the user choses 0
        if user_choice == 0:
            print("GoodBye!")
            break

        # to select the folder using the folder_selector.py
        elif user_choice == 1:
            selected_path = select_folder()
            # checking if the user canceled mid way without selection anything
            if selected_path:
                # reseting the data if the folder is changed
                folder_path = selected_path
                scanned_data = None
                identified_file_type = None
                scanned_folder = None
                print(folder_path)
            else:
                # showing an error if no folder is selected
                print(f"No folder selected. Current folder - {folder_path}")

        # to scan the folder if it has not been scanned before
        elif user_choice == 2:
            # checking if the user has selected a folder or not
            if folder_path is None or folder_path == "":
                print("Select a folder before performing any action")
                continue

            # only running the scan on this folder if it has not alredy been scanned before
            if scanned_data is None or not already_scanned(folder_path, scanned_folder):
                print("Scanning...")  # Loading message
                scanned_data = scan_folder(
                    folder_path
                )  # storing the data from the scan in scanned_data
                scanned_folder = Path(folder_path).resolve()
                print("Identifying type of file...")  # Loading message
                identified_file_type = scan_file_signiture(
                    scanned_data
                )  # storing the data of file typr in identified_file_type
                print("\n==============================")
                print("        Scanned Report")
                print("==============================")
                print(f"Files found: {len(scanned_data)}\n")

                for (
                    file_type,
                    files,
                ) in identified_file_type.items():  # showing the file type data
                    print(f"{file_type} files: {len(files)}")
                print()

                # file.relative_to(folder_path) displays the subfolder too with the file (knowladge)
                for index, file in enumerate(
                    scanned_data, start=1
                ):  # printing all the files in the folder
                    print(f"{index}. {file.name}")

            # not running the scan if this file has already been scanned
            else:
                print("\n==============================")
                print("        Scanned Report")
                print("==============================")
                print(f"Files found: {len(scanned_data)}\n")

                for file_type, files in identified_file_type.items():
                    print(f"{file_type} files: {len(files)}")
                print()

                for index, file in enumerate(scanned_data, start=1):
                    print(f"{index}. {file.name}")

        # to check for duplicate files in the folder
        elif user_choice == 3:
            if folder_path is None or folder_path == "":
                print("Select a folder before performing any action")
                continue
            if scanned_data is None or not already_scanned(folder_path, scanned_folder):
                scanned_data = None
                print("Scanning the folder...")
                scanned_data = scan_folder(folder_path)
                scanned_folder = Path(folder_path).resolve()

            print("Finding dublicates...")  # Loading message

            duplicate_list = find_dublicate(
                scanned_data
            )  # storing the data in dublicate_list
            print("\n==============================")
            print("      Duplicate Report")
            print("==============================")
            print(f"Dublicates found: {len(duplicate_list)}")

            for index, duplicate in enumerate(
                duplicate_list, start=1
            ):  # looping through the duplicate_list
                print(f"{index} :->")
                for i, file in enumerate(
                    duplicate
                ):  # looping through each duplicate file in the diplicate_list
                    clean_path = file.relative_to(folder_path)

                    # Use └── for the very last item in the tree, ├── for others
                    branch = "└──" if i == len(duplicate) - 1 else "├──"

                    print(f"  {branch} {file.name} ({clean_path})")

        # to give an orgainzation plan
        elif user_choice == 4:
            if not folder_path:
                print("Select a folder before performing any action")
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

            if not identified_file_type:
                identified_file_type = None
                print("Identifying type of file...")
                identified_file_type = scan_file_signiture(scanned_data)
            print("Creating a plan...")
            organization_plan = create_organization_plan(
                identified_file_type, destination_folder
            )

            print("\n==============================")
            print("       Organization Plan")
            print("==============================")

            for destination_path, files in organization_plan.items():
                print(f"\n📁{destination_path.name}/ {len(files)} files.")

                for i, file in enumerate(files):
                    branch = "└──" if i == len(files) - 1 else "├──"
                    print(f"\t{branch} {file.relative_to(Path(folder_path))}")

            # asking the user for conformation to make changes to the folder
            user_conformation = None
            try:
                while True:
                    user_conformation = str(input("Conform this plan: (y/n)"))

                    if user_conformation == "y" or user_conformation == "n":
                        break
            except OSError as error:
                print(f"Invalid input!: {error}")

        elif user_choice == 5:
            print("Option 5")
        elif user_choice == 6:
            print("Option 6")
        elif user_choice == 7:
            print("Option 7")


if __name__ == "__main__":
    main()
