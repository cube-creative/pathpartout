from pathpartout.api import config
import logging


class TreePath:
    """Model-Presenter object able to give information relative to a part-partout configuration file.

    Note:
        Use function in api/tree module to have an instance of TreePath

    Attributes:
        available_info (list(str)): Info names available to use in the current config of the TreePath.
        available_labels (list(str)): Label names available to use in the current config of the TreePath.
        info (dict(str)): info use in the current config of the TreePath with its values (None par default).
        config_filepath (str): configuration filepath path_partout.conf currently used.
    """

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
        """Edit multiple info with given dict.

        Args:
            new_info(dict(str)): info to add of the tree.

        """
        for info_name, value in new_info.items():
            if info_name in self.available_info:
                self.info[info_name] = value
            else:
                logging.warning(f"{info_name} is not an available information in configuration: {self.config_filepath}")

    def get_label_path(self, label_name):
        """Get path associated to the given label.

        If info needed for building the path are missing, raise an error that specify the missing info.

        Returns:
            str: path associated to the label.

        """
        if label_name not in self._available_labels:
            raise ValueError("Path Partout : Given label doesn't exist in the current config.")
        else:
            info = {k: v for (k, v) in self.info.items() if k in self._available_info and v is not None}
            return config.find_label_path(self._config_filepath, label_name, info)
