from pathpartout.application.use_cases import tree_base_builder, tree_base_getter


def get_required_info(config_path):
    """Get dict of required info to generate the base of the arbo of the config given filepath.

        Args:
            config_path (str): Path of the configuration file to consider.

        Returns:
            dict: keys are names of required info. values are all None.

    """
    required_info_list = tree_base_getter.get_required_tree_base_info(config_path)
    return {info: None for info in required_info_list}


def generate(config_path, required_info):
    """Generate the base for new project folder architecture depending on the given config path.

        Args:
            config_path (str): Path of the configuration file to consider.
            required_info (dict) : info used to generate the base folder architecture.
                see get_required_info() request to have required info empty dict.

    """
    tree_base_builder.build_tree_base(config_path, required_info)
