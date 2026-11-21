import hashlib
from pathlib import Path


def calculate_hash(file_path):
    target_file = Path(
        file_path
    )  # to get a clear path of the file using the pathlib.Path
    hasher = hashlib.sha256()  # creating a new hash

    try:
        with open(target_file, "rb") as file_byte:
            while True:  # running this loop until the whole file is hashed
                chunk = file_byte.read(
                    4096
                )  # getting only a small portion of the bytes to save memory

                if not chunk:  # breaking the loop if the whole file is been read
                    break

                hasher.update(
                    chunk
                )  # adding the chunks to the hasher without loosing anything
        return hasher.hexdigest()
    except PermissionError as error:
        print(f"{target_file.name} Error: {error}")
        return None
    except OSError as error:
        print(f"{target_file.name} Error: {error}")
        return None
