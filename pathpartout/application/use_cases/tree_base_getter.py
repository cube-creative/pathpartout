from pathpartout.application.use_cases import config_path_finder, config_reader
from pathpartout.application.entities import TreeArchitecture


def get_tree_base(path, info_needed):
    config_filepath = config_path_finder.find_from_path(path)
    config = config_reader.read_from_filepath(config_filepath)
    tree_architecture = TreeArchitecture.build_from_config(config)
    missing_info_names = [info for info in tree_architecture.auto_arbo_info_names if info not in info_needed.keys()]
    if missing_info_names:
        raise ValueError(f"Missing info needed to create base tree structure : {' '.join(missing_info_names)}")
    return tree_architecture.get_all_filled_paths_with_given_info(info_needed)


def get_tree_base_info_needed(path):
    config_filepath = config_path_finder.find_from_path(path)
    config = config_reader.read_from_filepath(config_filepath)
    return TreeArchitecture.build_from_config(config).auto_arbo_info_names
