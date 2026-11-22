import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


def move_file(source, destination):
    source = Path(source)
    destination = Path(destination)

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"Error in {destination}: {error}")
        logger.error(f"Failed to create a folder at - {destination}")
        return False

    target = destination / source.name

    try:
        counter = 1
        while target.exists():
            target = destination / f"{source.stem}_{counter}{source.suffix}"
            counter += 1
        shutil.move(str(source), str(target))
        return True
    except OSError as error:
        print(f"Error moving {source.name}! {error}")
        logger.error(f"Failed to move file - {source}")
        return False
