import os
import re
import yaml
import logging
from pathpartout.application.entities import Configuration


def read_from_filepath(config_filepath):
    config_data = _open_config_file(config_filepath)
    if not _is_valid_config_data(config_data):
        raise ValueError("Config {config_filepath} has incorrect syntax.".format(config_filepath=config_filepath))
    config = Configuration(config_filepath, config_data)
    _resolve_links(config, config_data)
    return config


def read_scopes(config_filepath):
    config_data = _open_config_file(config_filepath)
    if not config_data:
        return list()
    return config_data.get("scopes", list())


def read_name(config_filepath):
    config_data = _open_config_file(config_filepath)
    if not config_data:
        return None
    return config_data.get("name", list())


def read_search_terms(config_filepath):
    config_data = _open_config_file(config_filepath)
    if not config_data:
        return dict()
    return config_data.get("search_terms", dict())


def is_valid_config_filepath(filepath):
    return _is_valid_config_data(_open_config_file(filepath))


def _resolve_links(config, config_data):
    if not config_data.get("linked"):
        return
    for linked_config_filepath in config_data.get("linked"):
        linked_config_data = _open_config_file(linked_config_filepath)
        if not _is_valid_config_data(linked_config_data):
            raise ValueError("Linked configuration {linked_config_filepath} has invalid syntax.")
        config.extend_with_linked_data(linked_config_data)


ROOT_MATCHER = re.compile("\{\{root:([\w]+)*\}\}")


def _get_platform_roots():
    """ Get the platform roots from the environment variable PATH_PARTOUT_ROOTS

    Returns:
        list: list of dictionnary with root label and path else None
    """ 
    plateform_roots = os.environ.get('PATH_PARTOUT_ROOTS', None)
    if not plateform_roots:
        return None
    plaform_roots_regex = re.compile("(?P<label>[^=&]+)=(?P<path>[^=&]+)")
    
    return {match.groupdict().get('label'):match.groupdict().get('path') for match in plaform_roots_regex.finditer(plateform_roots)}


def _resolve_roots(config_data):
    platform_roots = _get_platform_roots()
    
    # Resolve scopes
    for index, scope in enumerate(config_data.get("scopes")):
        match = ROOT_MATCHER.match(scope)
        if match:
            root_label = match.group(1)
            root_path = platform_roots.get(root_label)
            if root_path is None:
                raise ValueError(f"Root label {root_label} not defined (set it in PATH_PARTOUT_ROOTS environment variable)")
            else:
                config_data['scopes'][index] = scope.replace("{{"+f"root:{root_label}"+"}}", root_path)

    # Resolve trees
    # TODO: Use this in concepual path instead ?
    for tree_index, tree in enumerate(config_data.get("trees")):
        tree_root = next(iter(tree))
        tree_content = tree.get(tree_root)
        match = ROOT_MATCHER.match(tree_root)
        if match:
            config_data['trees'][tree_index] = {platform_roots.get(match.group(1)) : tree_content}


def _open_config_file(config_filepath):
    try:
        with open(config_filepath, "r") as config_stream:
            # TODO: An idea, use Yaml builtin functions
            config = yaml.safe_load(config_stream)
            
            _resolve_roots(config)
            return config
    except Exception as e:
        logging.warning(e)
        return None


def _is_valid_config_data(config_data):
    return config_data and Configuration.is_valid_conf_data(config_data)
