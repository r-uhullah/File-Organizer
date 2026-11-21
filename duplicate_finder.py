from pathlib import Path

from hasher import calculate_hash


def find_dublicate(file_path):
    folder = Path(file_path)
    saved_hashes = {}

    for item in folder.rglob("*"):
        if not item.is_file():
            continue
        file_hash = calculate_hash(item)

        if file_hash is None:
            continue

        saved_hashes.setdefault(file_hash, []).append(item)

    duplicates = []

    for file_hash, files in saved_hashes.items():
        if len(files) > 1:
            duplicates.append(files)
    return duplicates
