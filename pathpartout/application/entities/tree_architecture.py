from .tree_node import TreeNode


class TreeArchitecture:
    def __init__(self):
        self.auto_arbo_info_names = None
        self.trees = set()

    @staticmethod
    def build_from_config(architecture_config):
        tree_architecture = TreeArchitecture()
        if not isinstance(architecture_config, dict):
            raise ValueError("Path Partout: Architecture config should be dictionary")
        tree_architecture.auto_arbo_info_names = architecture_config.pop("auto_arbo", None)
        for tree_name, tree_content in architecture_config.items():
            tree_architecture.trees.add(TreeNode.build_from_config(tree_name, tree_content))
        return tree_architecture

    def find_label_filepath(self, label_name):
        for tree in self.trees:
            filepath = tree.find_label_filepath(label_name, list())
            if filepath:
                return filepath

    def get_all_path_labels(self):
        path_labels = dict()
        for tree in self.trees:
            tree.get_all_path_labels(path_labels, list())
        return path_labels

    def get_all_filled_paths_with_given_info(self, info):
        paths = list()
        for tree in self.trees:
            tree.get_all_filled_paths_with_given_info(paths, list(), info)
        return list(set(paths))
