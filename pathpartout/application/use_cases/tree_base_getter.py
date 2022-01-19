from pathpartout.application.use_cases import config_path_finder, config_reader
from pathpartout.application.entities import TreeArchitecture


def get_tree_base(config_filepath, required_info):
    config = config_reader.read_from_filepath(config_filepath)
    missing_info_names = [info for info in config.auto_arbo_required_info if info not in required_info.keys()]
    if missing_info_names:
        raise ValueError("Missing required info to create base tree structure : {missing_info_names}".format(
            missing_info_names=' '.join(missing_info_names)
        ))
    tree_architecture = TreeArchitecture.build_from_config(config)
    return tree_architecture.get_all_filled_paths_with_given_info(required_info)


def get_required_tree_base_info(config_filepath):
    config = config_reader.read_from_filepath(config_filepath)
    return config.auto_arbo_required_info
