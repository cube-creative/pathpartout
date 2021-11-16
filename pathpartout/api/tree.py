from pathpartout.application.use_cases import tree_builder
from pathpartout.infrastructure.path_tree_presenter import TreePathPresenter


def get_from_label(label_name, filepath):
    """Find config associated to the given filepath and get a TreePath object with info and labels relative to it.

    This request return a Model-Presenter TreePath, with many method to interact with the api.
    See TreePath definition for more information.

    Args:
        label_name (str): The label of the config used to define tree.
        filepath (str): The filepath corresponding to the given label.

    Returns:
        TreePath corresponding to the config file found and the given information.

    """
    tree_path_presenter = TreePathPresenter()
    tree_builder.build_from_label(tree_path_presenter, label_name, filepath)
    return tree_path_presenter.tree_path


def get_from_shot_working_filepath(filepath):
    """Find config associated to the given filepath and get a TreePath object with info of the label "shot_working_file".

    This request return a Model-Presenter TreePath, with many method to interact with the api.
    See TreePath definition for more information.

    Args:
        filepath (str): The filepath of the shot working file.

    Returns:
        TreePath corresponding to the config file found and the given filepath.

    """
    tree_path_presenter = TreePathPresenter()
    tree_builder.build_from_label(tree_path_presenter, "shot_working_file", filepath)
    return tree_path_presenter.tree_path
