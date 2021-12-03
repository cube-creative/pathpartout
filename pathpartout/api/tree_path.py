from pathpartout.api import config
import logging


class TreePath:
    def __init__(self):
        self.info = dict()
        self._available_info = list()
        self._available_labels = list()
        self._config_filepath = str()

    @property
    def available_info(self):
        return self._available_info

    @property
    def available_labels(self):
        return self._available_labels

    @property
    def config_filepath(self):
        return self._config_filepath

    def populate_info(self, new_info):
        for info_name, value in new_info.items():
            if info_name in self.available_info:
                self.info[info_name] = value
            else:
                logging.warning(f"{info_name} is not an available information in configuration: {self.config_filepath}")

    def get_label_path(self, label_name):
        if label_name not in self._available_labels:
            raise ValueError("Path Partout : Given label doesn't exist in the current config.")
        else:
            info = {k: v for (k, v) in self.info.items() if k in self._available_info and v is not None}
            return config.find_label_path(self._config_filepath, label_name, info)
