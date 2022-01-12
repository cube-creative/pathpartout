from pathpartout.application.use_cases import aggregate_getter, info_getter


def get(name, config_filepath, info):
    return aggregate_getter.get_from_config(name, config_filepath, info)


def get_info_from_aggregate(config_filepath, aggregate, value):
    return info_getter.get_info_from_aggregate(config_filepath, aggregate, value.lower())
