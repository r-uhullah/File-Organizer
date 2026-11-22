import logging
from tkinter import Tk, filedialog

logger = logging.getLogger(__name__)


def select_folder():
    root = Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory(title="Select a folder to organize")

    root.destroy()
    return folder_path
