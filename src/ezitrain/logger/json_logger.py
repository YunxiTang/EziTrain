import json
from .base_logger import BaseLogger


class JsonLogger(BaseLogger):
    """
    Json Logger: log simple data into json file
    """

    def __init__(self, path_to_save: str, name: str = None):
        super().__init__(path_to_save, name)
        self.check_dir(path_to_save)
        self._dict_data = dict()

    def log_kv(self, k: str, v):
        self._dict_data[k] = v

    def log_dict_data(self, dict_data):
        for key, val in dict_data.items():
            self._dict_data[key] = val

    def save_data(self):
        with open(self._path, "w") as f:
            json.dump(self._dict_data, f, indent=4)
        return
