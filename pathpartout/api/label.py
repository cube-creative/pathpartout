from pathpartout.application.use_cases import path_finder, info_getter


def find_label_path(config_filepath, label_name, info):
    """Get the filepath associated with the label name, using given config file and information

    Args:
        config_filepath (str): The filepath of the Path Partout configuration file to use.
        label_name (str): The label name corresponding to the filepath to found in the configuration.
        info (dict of str): Information to include in the configuration.

    Returns:
        str: filepath corresponding to the given label name.

    """
    return path_finder.find_from_label(config_filepath, label_name, info)


def get_info_from_label(config_filepath, label, path):
    """Get info extracted from the given label path, depending on the given configuration.

    Args:
        config_filepath (str): The filepath of the Path Partout configuration file to use.
        label (str): The label name corresponding to the filepath to use in the configuration.
        path (str): Path from which extract data.

    Returns:
        dict(str, int): info extracted from the path.

    """
    return info_getter.get_from_label(config_filepath, label, path)
