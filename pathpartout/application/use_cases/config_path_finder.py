import os
from pathpartout.application.use_cases import config_reader

CONFIG_FILE_NAME = "path_partout.conf"


def find_from_path(path):
    if os.path.isdir(path) and _has_valid_config_file(path):
        return os.path.join(path, CONFIG_FILE_NAME).replace('\\', '/')

    while not _is_file_system_root(path):
        path = os.path.dirname(path)
        if _has_valid_config_file(path):
            return os.path.join(path, CONFIG_FILE_NAME).replace('\\', '/')
    raise ValueError("Path Partout: Given filepath doesn't have associate config file.")


def is_valid_config_file(filepath):
    return config_reader.read_from_filepath(filepath)


def _is_file_system_root(path):
    return os.path.dirname(path) == path


def _has_valid_config_file(path):
    config_file_path = os.path.join(path, CONFIG_FILE_NAME).replace('\\', '/')
    if os.path.exists(config_file_path) and is_valid_config_file(config_file_path):
        return True
    return False




