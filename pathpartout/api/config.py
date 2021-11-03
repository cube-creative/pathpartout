from pathpartout.application.use_cases import path_finder


def find_label_path(config_filepath, label_name, info):
    return path_finder.find_from_label(config_filepath, label_name, info)
