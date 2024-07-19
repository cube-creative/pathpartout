import yaml
import logging
from pathpartout.application.entities import Configuration
from functools import cache

@cache
def read_from_filepath(config_filepath):
    config_data = _open_config_file(config_filepath)
    if not _is_valid_config_data(config_data):
        raise ValueError("Config {config_filepath} has incorrect syntax.".format(config_filepath=config_filepath))
    config = Configuration(config_filepath, config_data)
    _resolve_links(config, config_data)
    return config

@cache
def read_scopes(config_filepath):
    config_data = _open_config_file(config_filepath)
    if not config_data:
        return list()
    return config_data.get("scopes", list())

@cache
def read_name(config_filepath):
    config_data = _open_config_file(config_filepath)
    if not config_data:
        return None
    return config_data.get("name", list())

@cache
def read_search_terms(config_filepath):
    config_data = _open_config_file(config_filepath)
    if not config_data:
        return dict()
    return config_data.get("search_terms", dict())

@cache
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


def _open_config_file(config_filepath):
    try:
        with open(config_filepath, "r") as config_stream:
            return yaml.safe_load(config_stream)
    except Exception as e:
        logging.warning(e)
        return None


def _is_valid_config_data(config_data):
    return config_data and Configuration.is_valid_conf_data(config_data)
