from pathpartout.application.entities import TreeArchitecture, ConceptualPath
from pathpartout.application.use_cases import config_path_finder, config_reader


def build_from_label(tree_presenter, label, path):
    config_filepath = config_path_finder.find_from_path(path)
    config = config_reader.read_from_filepath(config_filepath)
    tree_presenter.set_config_info(config.name, config.filepath, config.aggregates_names)
    tree_architecture = TreeArchitecture.build_from_config(config)
    labels_paths = tree_architecture.get_all_path_labels()
    if not labels_paths.get(label):
        raise ValueError(
            "Path Partout: Given filepath doesn't have {label} label in its config file : {config_filepath}.".format(
                label=label,
                config_filepath=config_filepath
            ))
    tree_presenter.set_labels(list(labels_paths.keys()))
    info = ConceptualPath.get_all_empty_info(labels_paths.values())
    info.update(labels_paths.get(label).extract(path))
    tree_presenter.set_info(info)


def build_from_path(tree_presenter, path):
    config_filepath = config_path_finder.find_from_path(path)
    build_from_config(tree_presenter, config_filepath)


def build_from_config(tree_presenter, config_filepath):
    config = config_reader.read_from_filepath(config_filepath)
    tree_presenter.set_config_info(config.name, config.filepath, config.aggregates_names)

    tree_architecture = TreeArchitecture.build_from_config(config)
    labels_paths = tree_architecture.get_all_path_labels()
    tree_presenter.set_labels(list(labels_paths.keys()))

    info = ConceptualPath.get_all_empty_info(labels_paths.values())
    tree_presenter.set_info(info)


