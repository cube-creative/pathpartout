import yaml


def read_from_filepath(config_filepath):
    config_data = _open_config_file(config_filepath)
    _append_linked_config(config_data)
    return config_data


def _append_linked_config(config_data):
    if not config_data.get("linked"):
        return
    for linked_config_filepath in config_data.get("linked"):
        linked_config_data = _open_config_file(linked_config_filepath)
        linked_config_data.pop('linked', None)
        config_data.update(linked_config_data)
    config_data.pop('linked', None)


def _open_config_file(config_filepath):
    try:
        with open(config_filepath, "r") as config_stream:
            return yaml.safe_load(config_stream)
    except yaml.YAMLError as e:
        print(f"No valid tree structure configuration into {config_filepath} :\n{e}")