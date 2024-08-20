import os
from pathpartout.application.use_cases import config_reader
ENV_CONFIG_FOLDERS_NAME = "PATH_PARTOUT_CONF_FOLDERS"


def set_config_folders(folders_paths):
    for path in folders_paths:
        if not os.path.isdir(path):
            raise ValueError("Config Folder {path} does not exist.".format(path=path))
    os.environ[ENV_CONFIG_FOLDERS_NAME] = ";".join(folders_paths)


def get_conf_from_folders():
    conf_file_paths = list()
    if os.environ.get(ENV_CONFIG_FOLDERS_NAME):
        folders_paths = os.environ[ENV_CONFIG_FOLDERS_NAME].split(";")
        for folder in folders_paths:
            conf_file_paths.extend(get_conf_from_folder(folder))
    return conf_file_paths


def get_conf_from_folder(folder_path):
    conf_files_paths = list()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if os.path.splitext(file)[1] == ".conf":
                conf_files_paths.append(os.path.join(root, file).replace("\\", "/"))
    return conf_files_paths


def get_all_names():
    return list(get_config_paths_by_names().keys())


def get_config_paths_by_scopes():
    conf_files_paths = get_conf_from_folders()

    conf_scopes = dict()
    for filepath in conf_files_paths:
        for scope in config_reader.read_scopes(filepath):
            conf_scopes[scope] = filepath
    return conf_scopes


def get_config_paths_by_names():
    conf_files_paths = get_conf_from_folders()

    names = dict()
    for filepath in conf_files_paths:
        name = config_reader.read_name(filepath)
        if name:
            names[name] = filepath
    return names


def get_config_paths_by_search_term_values(search_term):
    conf_files_paths = get_conf_from_folders()
    values = dict()
    for filepath in conf_files_paths:
        search_terms = config_reader.read_search_terms(filepath)
        if search_terms.get(search_term):
            for items in search_terms[search_term]:
                values[items] = filepath
    return values
