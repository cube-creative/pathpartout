import yaml


def read_from_filepath(config_filepath):
    try:
        with open(config_filepath, "r") as config_stream:
            return yaml.safe_load(config_stream)
    except yaml.YAMLError as e:
        print(f"No valid tree structure configuration into {config_filepath} :\n{e}")
