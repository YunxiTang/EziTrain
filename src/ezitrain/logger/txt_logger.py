import logging
from .base_logger import BaseLogger


def create_local_logger(path_to_save):
    """
    Create a logger that writes to a log file and stdout.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[\033[34m%(asctime)s\033[0m] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(), logging.FileHandler(path_to_save)],
    )
    logger = logging.getLogger(__name__)
    return logger


class TxtLogger(BaseLogger):
    def __init__(self, path_to_save: str, name: str = None):
        super().__init__(path_to_save, name)
        self._logger = create_local_logger(path_to_save)

    def log(self, msg: str):
        self._logger.info(msg)

    def save_data(self):
        return
