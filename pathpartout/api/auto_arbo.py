from pathpartout.application.use_cases import tree_base_builder, tree_base_getter


def get_info_needed(config_path):
    """Get dict of needed info to generate the base of the arbo of the config given filepath.

        Args:
            config_path (str): Path of the configuration file to consider.

        Returns:
            dict: keys are names of info needed. values are all None.

    """
    info_needed_list = tree_base_getter.get_tree_base_info_needed(config_path)
    return {info: None for info in info_needed_list}


def generate(config_path, info_needed):
    """Generate the base for new project folder architecture depending on the given config path.

        Args:
            config_path (str): Path of the configuration file to consider.
            info_needed (dict) : info used to generate the base folder architecture.
                see get_info_needed() request to have info needed empty dict.

    """
    tree_base_builder.build_tree_base(config_path, info_needed)
