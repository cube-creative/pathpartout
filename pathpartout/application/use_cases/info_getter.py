from pathpartout.application.entities import TreeArchitecture, ConceptualPath
from pathpartout.application.use_cases import config_reader


def get_from_label(config_filepath, label, path):
    config = config_reader.read_from_filepath(config_filepath)
    tree_architecture = TreeArchitecture.build_from_config(config)
    return get_label_info_from_tree(tree_architecture, label, path)


def get_from_aggregate(config_filepath, aggregate, value):
    config = config_reader.read_from_filepath(config_filepath)
    if aggregate not in config.aggregates_names:
        raise ValueError("Aggregate {aggregate} doesn't exist in conf : {config_filepath}".format(
            aggregate=aggregate,
            config_filepath=config_filepath
        ))
    return ConceptualPath([config.aggregates[aggregate]]).extract(value)


def get_label_info_from_tree(tree, label, path):
    labels_paths = tree.get_all_path_labels()
    if not labels_paths.get(label):
        raise ValueError(
            "Path Partout: Given filepath doesn't have {label} label in its config file : {filepath}.".format(
                label=label,
                filepath=tree.config.filepath
            )
        )
    return labels_paths.get(label).extract(path)
