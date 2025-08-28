"""
    Loggers Template
"""
import os


class BaseLogger:
    '''
        base logger class
    '''
    def __init__(self, path_to_save, name: str = None):
       directory = os.path.dirname(path_to_save)
       if not os.path.exists(directory):
            print("Making new directory at {}".format(directory))
            os.makedirs(directory)
       self._directory = directory
       self._path = path_to_save
       self._logger_name = name

    @property
    def logger_name(self):
        return self._logger_name