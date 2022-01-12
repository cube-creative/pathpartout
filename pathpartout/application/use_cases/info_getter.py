from pathpartout.application.entities import TreeArchitecture, ConceptualPath
from pathpartout.application.use_cases import config_reader


def get_info_from_label(config_filepath, label, path):
    config = config_reader.read_from_filepath(config_filepath)
    tree_architecture = TreeArchitecture.build_from_config(config)
    labels_paths = tree_architecture.get_all_path_labels()
    if not labels_paths.get(label):
        raise ValueError(
            f"Path Partout: Given filepath doesn't have {label} label in its config file : {config_filepath}.")

    return labels_paths.get(label).extract(path)


def get_info_from_aggregate(config_filepath, aggregate, value):
    config = config_reader.read_from_filepath(config_filepath)
    if aggregate not in config.aggregates_names:
        raise ValueError(f"Aggregate {aggregate} doesn't exist in conf : {config_filepath}")
    return ConceptualPath([config.aggregates[aggregate]]).extract(value)
