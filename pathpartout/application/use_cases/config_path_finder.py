import os
from pathpartout.application.use_cases import config_reader

CONFIG_FILE_NAME = "path_partout.conf"


def find_from_filepath(filepath):
    while not _is_file_system_root(filepath):
        filepath = os.path.dirname(filepath)
        if _has_valid_config_file(filepath):
            return os.path.join(filepath, CONFIG_FILE_NAME).replace('\\', '/')
    return None


def _is_file_system_root(path):
    return os.path.dirname(path) == path


def _has_valid_config_file(path):
    config_file_path = os.path.join(path, CONFIG_FILE_NAME).replace('\\', '/')
    if os.path.exists(config_file_path) and _is_valid_config_file(config_file_path):
        return True
    return False


def _is_valid_config_file(filepath):
    return config_reader.read_from_filepath(filepath)

