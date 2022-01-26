from pathpartout.api import config_folders, aggregate, label
import logging


class TreePath:
    """Model-Presenter object able to give information relative to a part-partout configuration file.

    Note:
        Use function in api/tree module to have an instance of TreePath

    Attributes:
        available_info (list(str)): Info names available to use in the current config of the TreePath.
        available_labels (list(str)): Label names available to use in the current config of the TreePath.
        info (dict(str)): info use in the current config of the TreePath with its values (None par default).
        aggregates (list(str)): aggregates names of the config of the TreePath.
        config_filepath (str): configuration filepath path_partout.conf currently used.
        name (str) : names of the config of the TreePath.
    """

    def __init__(self):
        self.info = dict()
        self._name = None
        self._aggregates = list()
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

    @property
    def aggregates(self):
        return self._aggregates

    @property
    def name(self):
        return self._name

    def populate_info(self, new_info):
        """Edit multiple info with given dict.

        Args:
            new_info(dict(str)): info to add of the tree.

        """
        for info_name, value in new_info.items():
            if info_name in self.available_info:
                self.info[info_name] = value
            else:
                logging.warning(
                    "{info_name} is not an available information in configuration: {config_filepath}".format(
                        info_name=info_name,
                        config_filepath=self.config_filepath
                    ))

    def get_label_path(self, label_name):
        """Get path associated to the given label.

        If required info for building the path are missing, raise an error that specify the missing info.

        Args:
            label_name(str): name of the label that we want the path.

        Returns:
            str: path associated to the label.

        """
        if label_name not in self._available_labels:
            raise ValueError("Path Partout : Given label doesn't exist in the current config.")
        else:
            info = {k: v for (k, v) in self.info.items() if k in self._available_info and v is not None}
            return label.find_label_path(self._config_filepath, label_name, info)

    def get_aggregate(self, name):
        """Get aggregate value with the given name, computed with the current info.

        Args:
            name(str): name of the wanted aggregate.

        Returns:
            str: data associated to the aggregate.

        """
        if name not in self._aggregates:
            raise ValueError(
                "Path Partout : Given aggregate {aggregate_name} doesn't exist in the current config.".format(
                    aggregate_name=name
                )
            )
        return aggregate.get(self.config_filepath, name, self.info)

    def fill_with_label(self, label_name, path):
        """Fill new data in the TreePath thanks to the given label path.

        Same as `tree.get_from_label()` but on existing TreePath.

        Args:
            label_name(str): name of the label that we give the path.
            path(str): path of the label from which new info are extracted.

        """
        info = label.get_info_from_label(self.config_filepath, label_name, path)
        self.info.update(info)

    def fill_with_aggregate(self, aggregate_name, value):
        """Fill new data in the TreePath thanks to the given aggregate value.

        Args:
            aggregate_name(str): name of the aggregate that we give the value.
            value(str): value of the aggregate from which new info are extracted.

        """
        info = aggregate.get_info_from_aggregate(self.config_filepath, aggregate_name, value)
        self.info.update(info)
