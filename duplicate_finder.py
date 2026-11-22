import logging

from hasher import calculate_hash  # calculates the hash of a single file

logger = logging.getLogger(__name__)


def find_dublicate(files_list):
    logger.info("Duplicate detection started")
    saved_hashes = (
        {}
    )  # to save the list of all the hashes with there files in a list if there are diplicates

    for (
        item
    ) in (
        files_list
    ):  # looping through the file list whcih is saved in the main after scanning the folder
        file_hash = calculate_hash(item)  # calculating the hash of the file

        if file_hash is None:
            continue

        saved_hashes.setdefault(file_hash, []).append(item)

    duplicates = []

    for (
        file_hash,
        files,
    ) in (
        saved_hashes.items()
    ):  # looping through the saved_hashes object to see if there is any hash with more then one file to its name if yes its added to the duplicate list
        if len(files) > 1:
            duplicates.append(files)

    logger.info("Duplicate files detected Sucessfully")
    return duplicates
