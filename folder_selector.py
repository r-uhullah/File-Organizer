import logging
from tkinter import Tk, filedialog

logger = logging.getLogger(__name__)


def select_folder():
    root = Tk()
    folder_path = None

    try:
        root.withdraw()

        folder_path = filedialog.askdirectory(title="Select a folder to organize")
    except OSError as error:
        print(f"Error selecting the file! {error}")
        logger.error("Failed to open the folder")
    finally:
        root.destroy()

    return folder_path
