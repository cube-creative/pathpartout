from pathpartout.application.use_cases import config_path_finder, config_reader
from pathpartout.application.entities import TreeArchitecture


def get_tree_base(config_filepath, info_needed):
    config = config_reader.read_from_filepath(config_filepath)
    missing_info_names = [info for info in config.auto_arbo_info if info not in info_needed.keys()]
    if missing_info_names:
        raise ValueError(f"Missing info needed to create base tree structure : {' '.join(missing_info_names)}")
    tree_architecture = TreeArchitecture.build_from_config(config)
    return tree_architecture.get_all_filled_paths_with_given_info(info_needed)


def get_tree_base_info_needed(config_filepath):
    config = config_reader.read_from_filepath(config_filepath)
    return config.auto_arbo_info
