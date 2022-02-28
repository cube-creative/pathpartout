from pathpartout.application.use_cases import config_reader
from pathpartout.application.entities import ConceptualPath


def get_from_config(name, config_path, info):
    config = config_reader.read_from_filepath(config_path)

    if name not in config.aggregates.keys():
        raise ValueError(
            "Path Partout : Given aggregate {aggregate_name} not found in config {config_path}.".format(
                aggregate_name=name,
                config_path=config.filepath
            )
        )
    return ConceptualPath([config.aggregates[name]]).fill(info, config_path)
