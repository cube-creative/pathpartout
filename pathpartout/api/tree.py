from pathpartout.application.use_cases import tree_builder
from pathpartout.infrastructure.path_tree_presenter import TreePathPresenter


def get_from_label(label, filepath):
    tree_path_presenter = TreePathPresenter()
    tree_builder.build_from_label(tree_path_presenter, label, filepath)
    return tree_path_presenter.tree_path


def get_from_shot_working_filepath(filepath):
    tree_path_presenter = TreePathPresenter()
    tree_builder.build_from_label(tree_path_presenter, "shot_working_file", filepath)
    return tree_path_presenter.tree_path
