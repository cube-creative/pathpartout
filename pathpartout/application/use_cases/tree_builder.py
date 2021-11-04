from pathpartout.application.entities import TreeArchitecture, ConceptualPath
from pathpartout.application.use_cases import config_path_finder, config_reader


def build_from_label(tree_presenter, label, filepath):
    config_filepath = config_path_finder.find_from_filepath(filepath)
    if not config_filepath:
        raise ValueError("Given filepath doesn't have associate config file.")
    tree_presenter.set_config_path(config_filepath)

    config = config_reader.read_from_filepath(config_filepath)
    tree_architecture = TreeArchitecture.build_from_config(config)
    labels_paths = tree_architecture.get_all_path_labels()
    if not labels_paths.get(label):
        raise ValueError(f"Given filepath doesn't have {label} label in its config file : {config_filepath}.")
    tree_presenter.set_labels(list(labels_paths.keys()))

    info = ConceptualPath.get_all_empty_info(labels_paths.values())
    info.update(labels_paths.get(label).extract(filepath))
    tree_presenter.set_info(info)
