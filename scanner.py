from pathlib import Path

EXCLUDED_FOLDERS = {
    "Images",
    "Documents",
    "Audio",
    "Archives",
    "Applications",
    "Fonts",
    "Databases",
    "Others",
}


def scan_folder(folder_path):
    folder = Path(folder_path)
    path_objects = []

    for item in sorted(folder.rglob("*")):
        if not item.is_file():
            continue

        relative_path = item.relative_to(folder)

        if any(parent in EXCLUDED_FOLDERS for parent in relative_path.parts[:-1]):
            continue

        path_objects.append(item)

    return path_objects
