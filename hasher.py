import hashlib
from pathlib import Path


def calculate_hash(file_path):
    target_file = Path(file_path)
    hasher = hashlib.sha256()

    try:
        with open(target_file, "rb") as file_byte:
            while True:
                chunk = file_byte.read(4096)

                if not chunk:
                    break

                hasher.update(chunk)
        return hasher.hexdigest()
    except PermissionError as error:
        print(f"{target_file.name} Error: {error}")
        return None
