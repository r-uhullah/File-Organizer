import logging


def setup_log():
    root_looger = logging.getLogger()

    if root_looger.hasHandlers():
        return

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s -",
        handlers=[logging.FileHandler("organizer.log", encoding="utf-8")],
    )
