import os
import logging
from pathpartout.application.use_cases import config_folders_reader, config_reader

CONFIG_FILE_NAME = "path_partout.conf"


def find_by_search_term(search_term, value):
    search_term_values = config_folders_reader.get_config_paths_by_search_term_values(search_term)

    for project_name, config_folder_path in search_term_values.items():
        if project_name.lower() == value.lower():
            return config_folder_path

    return None


def find_by_name(name):
    names = config_folders_reader.get_config_paths_by_names()
    return names.get(name, None)


def find_from_path(path):
    scopes = config_folders_reader.get_config_paths_by_scopes()
    path = os.path.dirname(path) if os.path.isfile(path) else path
    path = path.replace('\\', '/')
    while True:
        config_filepath = _search_valid_config_filepath(path, scopes)
        if config_filepath:
            return config_filepath

        path = os.path.dirname(path)
        if _is_file_system_root(path):
            config_filepath = _search_valid_config_filepath(path, scopes)
            if config_filepath:
                return config_filepath
            raise ValueError("Path Partout: Given filepath doesn't have associate config file : {config_filepath}"
                             .format(config_filepath=config_filepath))


def _search_valid_config_filepath(path, scopes=None):
    scopes = scopes or dict()
    config_filepath = scopes.get(path, None) or os.path.join(path, CONFIG_FILE_NAME).replace('\\', '/')
    if os.path.isfile(config_filepath):
        if config_reader.is_valid_config_filepath(config_filepath):
            return config_filepath
        logging.warning("Invalid configuration file found : {path}".format(path=config_filepath))


def _is_file_system_root(path):
    return os.path.dirname(path) == path







