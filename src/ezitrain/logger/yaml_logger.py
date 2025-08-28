import yaml
from .base_logger import BaseLogger


class YamlLogger(BaseLogger):
    '''
        Yaml Logger: log data into yaml file
    '''
    def __init__(self, path_to_save: str, name: str = None):
        super().__init__(path_to_save, name)
        self._dict_data = dict()

    def log_kv(self, k: str, v):
        self._dict_data[k] = v


    def log_dict_data(self, dict_data):
        for key, val in dict_data.items():
            self._dict_data[key] = val

    def save_data(self):
        with open(self._path, 'w') as f:
            yaml.dump(self._dict_data, f)
        return None