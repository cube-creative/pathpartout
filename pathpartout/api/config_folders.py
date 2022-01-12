from pathpartout.application.use_cases import config_path_finder, config_folders_reader


def set_paths(paths):
    config_folders_reader.set_configuration_folders(paths)


def get_config_path_by_name(name):
    return config_path_finder.find_by_name(name)


def search_config_path(search_term, value):
    return config_path_finder.find_by_search_term(search_term, value)


def get_all_config_names():
    return config_folders_reader.get_all_names()


#def get_scopes():
#    return config_reader.get_scopes_of_config_folders()
