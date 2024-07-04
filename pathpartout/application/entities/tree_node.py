from . import Label, ConceptualPath


class TreeNode:
    def __init__(
            self,
            name,
            children=None,
            labels=None):
        self.name = name
        self.children = children or set()
        self.labels = labels or set()

    @staticmethod
    def build_from_config(node_name, node_content):
        tree_node = TreeNode(node_name)
        for node_name, node_content in node_content.items():
            if isinstance(node_content, str):
                tree_node.labels.add(Label(name=node_name, filename_format=node_content))
            elif isinstance(node_content, dict):
                tree_node.children.add(TreeNode.build_from_config(node_name, node_content))
        return tree_node

    def get_all_path_labels(self, path_labels, parent_path_elements):
        path_elements = list(parent_path_elements)
        path_elements.append(self.name)

        for label in self.labels:
            path_labels[label.name] = ConceptualPath(path_elements + [label.filename_format])

        for child in self.children:
            child.get_all_path_labels(path_labels, path_elements)

    def find_label_filepath(self, label_name, parent_path_elements):
        path_elements = list(parent_path_elements)
        path_elements.append(self.name)

        label = self.get_label_from_name(label_name)
        if label:
            path_elements.append(label.filename_format)
            return ConceptualPath(path_elements)

        for child in self.children:
            path = child.find_label_filepath(label_name, path_elements)
            if path:
                return path

    def get_label_from_name(self, label_name):
        for label in self.labels:
            if label.name == label_name:
                return label
        return None

    def get_all_filled_paths_with_given_info(self, paths, parent_path, info, config_path):
        node_path = parent_path + [self.name]
        if not ConceptualPath(node_path).contains_info_needed(info):
            paths.append(ConceptualPath(parent_path).fill(info, config_path))
            return

        if not self.children:
            paths.append(ConceptualPath(node_path).fill(info, config_path))
            return

        for child in self.children:
            child.get_all_filled_paths_with_given_info(paths, node_path, info, config_path)
