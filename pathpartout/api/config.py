from pathpartout.application.use_cases import path_finder


def find_label_path(config_filepath, label_name, info):
    """Get the filepath associated with the label name, using given config file and information

    Args:
        config_filepath (str): The filepath of the Path Partout configuration file to use.
        label_name (str): The label name corresponding to the filepath to found in the configuration.
        info (dict of str): Information to include in the configuration.

    Returns:
        str: filepath corresponding to the given label name.

    """
    return path_finder.find_from_label(config_filepath, label_name.lower(), info)
