from pathlib import Path

FILE_CATEGORIES = {
    "JPEG": "Images",
    "PNG": "Images",
    "GIF": "Images",
    "BMP": "Images",
    "TIFF": "Images",
    "ICO": "Images",
    "PSD": "Images",
    "PDF": "Documents",
    "RTF": "Documents",
    "MP3": "Audio",
    "FLAC": "Audio",
    "OGG": "Audio",
    "ZIP": "Archives",
    "RAR": "Archives",
    "7Z": "Archives",
    "GZIP": "Archives",
    "BZIP2": "Archives",
    "XZ": "Archives",
    "EXE": "Applications",
    "ELF": "Applications",
    "TTF": "Fonts",
    "OTF": "Fonts",
    "SQLITE": "Databases",
}


def create_organization_plan(identified_files, destination_folder):
    organization_plan = {}

    for file_type, files in identified_files.items():
        category = FILE_CATEGORIES.get(file_type, "Others")

        destination_path = Path(destination_folder) / category

        organization_plan.setdefault(destination_path, []).extend(files)

    return organization_plan
