from pathpartout.application.use_cases import tree_builder
from pathpartout.infrastructure.path_tree_presenter import TreePathPresenter


def get_from_config(config_filepath):
    """Get a TreePath object corresponding to given config filepath with empty info and labels relative to it.

        This request return a Model-Presenter TreePath, with many method to interact with the api.
        See TreePath definition for more information.

        Args:
            config_filepath (str): The filepath of the config to use.

        Returns:
            TreePath corresponding to the given config.
        """
    if not config_filepath:
        raise ValueError("Path Partout: get_from_config need config_filepath argument")

    tree_path_presenter = TreePathPresenter()
    tree_builder.build_from_config(tree_path_presenter, config_filepath.lower())
    return tree_path_presenter.tree_path


def get_from_path(path):
    """Find config associated to the given path and get a TreePath object with empty info and labels relative to it.

        This request return a Model-Presenter TreePath, with many method to interact with the api.
        See TreePath definition for more information.

        Args:
            path (str): The path use to find the config.

        Returns:
            TreePath corresponding to the config file found.

        """
    if not path:
        raise ValueError("Path Partout: get_from_path need path argument")

    tree_path_presenter = TreePathPresenter()
    tree_builder.build_from_path(tree_path_presenter, path.lower())
    return tree_path_presenter.tree_path


def get_from_label(label_name, path):
    """Find config associated to the given path and get a TreePath object with info and labels relative to it.

    This request return a Model-Presenter TreePath, with many method to interact with the api.
    See TreePath definition for more information.

    Args:
        label_name (str): The label of the config used to define tree.
        path (str): The path corresponding to the given label.

    Returns:
        TreePath corresponding to the config file found and the given information.

    """
    if not path:
        raise ValueError("Path Partout: get_from_label need path argument")

    tree_path_presenter = TreePathPresenter()
    tree_builder.build_from_label(tree_path_presenter, label_name.lower(), path.lower())
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
    tree_builder.build_from_label(tree_path_presenter, "shot_working_file", filepath.lower())
    return tree_path_presenter.tree_path
