from pathpartout.application.presenter import TreePresenter
from pathpartout.api import config


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

    def get_label_path(self, label_name):
        if label_name not in self._available_labels:
            print("")
        else:
            info = {k: v for (k, v) in self.info.items() if k in self._available_info and v is not None}
            return config.find_label_path(self._config_filepath, label_name, info)


class TreePathPresenter(TreePresenter):
    def __init__(self):
        self._tree_path = TreePath()

    def set_info(self, info):
        self._tree_path.info = info
        self._tree_path._available_info = list(info.keys())

    def set_labels(self, labels):
        self._tree_path._available_labels = labels

    def set_config_path(self, config_path):
        self._tree_path._config_filepath = config_path

    @property
    def tree_path(self):
        return self._tree_path

