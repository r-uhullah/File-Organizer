import logging

logger = logging.getLogger(__name__)

FILE_SIGNATURES = {
    # Images
    "JPEG": [b"\xFF\xD8\xFF"],
    "PNG": [b"\x89PNG\r\n\x1A\n"],
    "GIF": [b"GIF8"],
    "BMP": [b"BM"],
    "TIFF": [b"II*\x00", b"MM\x00*"],
    "ICO": [b"\x00\x00\x01\x00"],
    "PSD": [b"8BPS"],
    # Documents
    "PDF": [b"%PDF"],
    "RTF": [b"{\\rtf"],
    # ZIP-based formats (need additional inspection to distinguish)
    "ZIP": [b"PK\x03\x04"],
    # Archives
    "RAR": [b"Rar!\x1A\x07"],
    "7Z": [b"7z\xBC\xAF\x27\x1C"],
    "GZIP": [b"\x1F\x8B"],
    "BZIP2": [b"BZh"],
    "XZ": [b"\xFD7zXZ\x00"],
    # Audio
    "MP3": [b"ID3"],  # ID3-tagged MP3 files
    "FLAC": [b"fLaC"],
    "OGG": [b"OggS"],
    # Executables and databases
    "EXE": [b"MZ"],
    "ELF": [b"\x7FELF"],
    "SQLITE": [b"SQLite format 3\x00"],
    # Fonts
    "TTF": [b"\x00\x01\x00\x00"],
    "OTF": [b"OTTO"],
}


def identify_file_type(file_signiture, file_item, results_dict):
    # looping over the dictionary to find the matching file signiture
    for file_type, signiture in FILE_SIGNATURES.items():
        # startswith() only works on typle or bytes not lists
        if file_signiture.startswith(tuple(signiture)):
            # appending the value to the results_dictionary if a file type is found
            results_dict.setdefault(file_type, []).append(file_item)
            return

    # appending the file to the unknown if none of the signitures match
    results_dict.setdefault("Unknown", []).append(file_item)


def scan_file_signiture(
    file_list,
):  # getting the already saved file from the main so that no new folder is scanned without any reason
    results_dict = {}
    for item in file_list:
        try:
            # reading the signiture of the file
            with open(item, "rb") as file:
                signiture = file.read(16)
                # calling the identify_file_type function to check the file type and append it to the result_dict
                identify_file_type(signiture, item, results_dict)
        except OSError as error:
            print(f"Could not read {item.name}: {error}")
            logger.error(f"Error reading file - {item.name}")

    return results_dict
