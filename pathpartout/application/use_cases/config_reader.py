import os
from pathlib import Path
import re
import yaml
import logging
from pathpartout.application.entities import Configuration
from functools import lru_cache
import os


def _optional_cache(func):
    if os.environ.get("PATHPARTOUT_ENABLE_CONF_CACHE", "false").lower() == "true":
        return lru_cache(maxsize=None)(func)
    return func

PLATFORM_ROOT_CONF_REGEX = re.compile("\{\{root:([\w]+)*\}\}") # {{root:label[?]}}
PLATFORM_ROOT_VARENV_REGEX = re.compile("(?P<label>[^=&]+)=(?P<path>[^=&]+)")


def _get_platform_roots():
    """ Get the platform roots from the environment variable PATH_PARTOUT_ROOTS

    Returns:
        list: list of dictionnary with root label and path else None
    """ 
    plateform_roots = os.environ.get('PATH_PARTOUT_ROOTS', None)
    if not plateform_roots:
        return None

    return {match.groupdict().get('label'):match.groupdict().get('path') for match in PLATFORM_ROOT_VARENV_REGEX.finditer(plateform_roots)}


def read_from_filepath(config_filepath):
    config_data = _open_config_file(config_filepath)
    if not _is_valid_config_data(config_data):
        raise ValueError("Config {config_filepath} has incorrect syntax.".format(config_filepath=config_filepath))
    _resolve_scope_roots(config_data)
    config = Configuration(config_filepath, config_data)
    _resolve_links(config, config_data)
    _resolve_tree_roots(config)
    return config


def read_scopes(config_filepath):
    config_data = _open_config_file(config_filepath)
    if not config_data:
        return list()
    _resolve_scope_roots(config_data)
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


def _resolve_path_root(path: str, platform_roots: dict):
    """ Resolve platform root in the path

    Args:
        path (str): The path to resolve
        platform_roots (dict): The platform roots

    Returns:
        str: The path with resolved root or None if no root to resolve
    """
    match = PLATFORM_ROOT_CONF_REGEX.match(path)
    if match:
        root_label = match.group(1)
        root_path = platform_roots.get(root_label)
        if root_path is None:
            raise ValueError(f"Root label {root_label} not defined (set it in PATH_PARTOUT_ROOTS environment variable)")
        return path.replace("{{"+f"root:{root_label}"+"}}", root_path)
    else:
        return None


def _resolve_tree_roots(config):
    """ Resolve trees's root by replacing the root label by the varenv value

    Args:
        config (Configuration): The configuration to resolve
    
    """
    platform_roots = _get_platform_roots()
    for tree_index, tree in enumerate(config.trees):
        tree_root = next(iter(tree))
        resolved_tree_root = _resolve_path_root(tree_root, platform_roots)
        if resolved_tree_root:
            tree_root_element = [*Path(resolved_tree_root).parts]
            # Expand root if needed
            root_patch =  tree.get(tree_root)
            for element in reversed(tree_root_element):
                root_patch = {element: root_patch}
                
            config.trees[tree_index] = root_patch


def _resolve_scope_roots(config_data):
    platform_roots = _get_platform_roots()
    for index, scope in enumerate(config_data.get("scopes")):
        resolved_scope_root = _resolve_path_root(scope, platform_roots)
        if resolved_scope_root:
            config_data['scopes'][index] = resolved_scope_root


@_optional_cache
def _open_config_file(config_filepath):
    try:
        with open(config_filepath, "r") as config_stream:
            return yaml.safe_load(config_stream)
    except Exception as e:
        logging.warning(e)
        return None


def _is_valid_config_data(config_data):
    return config_data and Configuration.is_valid_conf_data(config_data)
