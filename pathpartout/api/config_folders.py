from pathpartout.application.use_cases import config_path_finder, config_folders_reader


def set_paths(paths):
    """Set new paths for folders of configuration files.

    Edit the environment variable : PATH_PARTOUT_CONF_FOLDERS

    Args:
        paths (list(str)): Paths of folders to consider to find configuration file.
        label_name (str): The label name corresponding to the filepath to found in the configuration.
        info (dict of str): Information to include in the configuration.

    """
    config_folders_reader.set_config_folders(paths)


def get_config_path_by_name(name):
    """Get configuration filepath with the given name.

    Args:
        name (str): Name of the configuration.

    Returns:
        str: filepath of the configuration.

    """
    return config_path_finder.find_by_name(name)


def search_config_path(search_term, value):
    """Get configuration filepath with the searched value.

    Args:
        search_term (str): Name of the term to search value.
        value (str): Value to search.

    Returns:
        str: filepath of the configuration.

    """
    return config_path_finder.find_by_search_term(search_term, value)


def get_all_config_names():
    """Get all configuration files paths in the configuration folder by name

    Returns:
        dict(str): key: config name ; field: config filepath

    """
    return config_folders_reader.get_all_names()
