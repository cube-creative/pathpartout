from pathpartout.application.use_cases import tree_base_getter


def get_info_needed(path):
    """Find config associated to the given path and get dict of needed info to generate the base of the arbo.

        Args:
            path (str): The path use to find the config.

        Returns:
            dict: keys are names of info needed. values are all None.

    """
    return tree_base_getter.get_tree_base_info_needed(path)


def generate(path, info_needed):
    """Generate the base for new project folder architecture depending on the given config path.

        Args:
            path (str): The path use to find the config.
            info_needed (dict) : info used to generate the base folder architecture.
                see get_info_needed() request to have info needed empty dict.

        Returns:
            TreePath corresponding to the config file found.

    """

    return tree_base_getter.get_tree_base(path, info_needed)
