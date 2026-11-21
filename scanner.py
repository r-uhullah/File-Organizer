from pathlib import Path


def scan_folder(folder_path):
    folder = Path(folder_path)

    path_objects = []

    for item in sorted(folder.rglob("*")):
        if not item.is_file():
            continue

        path_objects.append(item)

    return path_objects
