from pathpartout.application.presenter import TreePresenter
from pathpartout.api.tree_path import TreePath


class TreePathPresenter(TreePresenter):
    def __init__(self):
        self._tree_path = TreePath()

    def set_info(self, info):
        self._tree_path.info = info
        self._tree_path._available_info = list(info.keys())

    def set_labels(self, labels):
        self._tree_path._available_labels = labels

    def set_config_info(self, name, path, aggregates):
        self._tree_path._name = name
        self._tree_path._config_filepath = path
        self._tree_path._aggregates = aggregates

    @property
    def tree_path(self):
        return self._tree_path

