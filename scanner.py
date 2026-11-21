from pathlib import Path


def scan_folder(folder_path):
    folder = Path(
        folder_path
    )  # converting the folder_path from the main to a proper pathlib.Path

    path_objects = []  # storing all the files path that are in the selected folder

    for item in sorted(
        folder.rglob("*")
    ):  # looping through all the items in the folder and also the items inside the subfolders (Recursive loop)
        if not item.is_file():
            continue

        path_objects.append(item)

    return path_objects
