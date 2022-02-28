from pathpartout.application.entities import TreeArchitecture
from pathpartout.application.use_cases import config_reader


def find_from_label(config_filepath, label_name, info):
    config = config_reader.read_from_filepath(config_filepath)
    tree_architecture = TreeArchitecture.build_from_config(config)
    concept_path = tree_architecture.find_label_filepath(label_name)
    return concept_path.fill(info, config_filepath)
