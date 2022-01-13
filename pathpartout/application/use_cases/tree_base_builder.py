import os
from pathpartout.application.use_cases import tree_base_getter


def build_tree_base(config_filepath, info_needed):
    paths_to_build = tree_base_getter.get_tree_base(config_filepath, info_needed)
    for path in paths_to_build:
        os.makedirs(path, exist_ok=True)
