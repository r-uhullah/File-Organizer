from folder_selector import select_folder  # to show the folder selection window
from scanner import (
    scan_folder,
)  # to scan the selected folder and get a list of all the files in it
from file_identifire import scan_file_signiture


def show_menu():
    print("==============================")
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
    # making folder_path avaliable for the main cause it need to used by all of the other option
    folder_path = None

    # keeps showing the menu until the user exits the program
    while True:
        user_choice = show_menu()

        if user_choice == 0:
            print("GoodBye!")
            break
        elif user_choice == 1:
            selected_path = select_folder()
            # checking if the user canceled mid way without selection anything
            if selected_path:
                folder_path = selected_path
                print(folder_path)
            else:
                print(f"No folder selected. Current folder - {folder_path}")

        elif user_choice == 2:
            # checking if the user has selected a folder or not
            if folder_path is None or folder_path == "":
                print("Select a folder before performing any action")
                continue
            # showing that the scanning has started if it takes time
            print("Scanning...")
            scanned_data = scan_folder(folder_path)
            identified_file_type = scan_file_signiture(folder_path)
            print("\nFiles found: ", len(scanned_data))

            # file.relative_to(folder_path) displays the subfolder too with the file
            for index, file in enumerate(scanned_data, start=1):
                print(f"{index}. {file.name}")

        elif user_choice == 3:
            print("Option 3")
        elif user_choice == 4:
            print("Option 4")
        elif user_choice == 5:
            print("Option 5")
        elif user_choice == 6:
            print("Option 6")
        elif user_choice == 7:
            print("Option 7")


if __name__ == "__main__":
    main()
