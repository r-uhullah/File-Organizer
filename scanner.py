import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def scan_folder(folder_path):
    logger.info(f"Scanning Stated - folder: {folder_path}")

    folder = Path(folder_path)
    path_objects = []

    for item in sorted(folder.rglob("*")):
        if not item.is_file():
            continue

        path_objects.append(item)

    logger.info(f"Scanning Finished - folder: {folder_path}")
    logger.info(f"Total files scanned {len(path_objects)}")

    return path_objects
