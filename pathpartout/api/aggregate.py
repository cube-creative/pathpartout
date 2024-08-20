from pathpartout.application.use_cases import aggregate_getter, info_getter


def get(config_filepath, name, info):
    """Get aggregate value with the given name in the given configuration, computed with given info.

        Args:
            config_filepath (str): Path of the configuration file to consider.
            name (str): Name of the wanted aggregate value.
            info (dict(str, int)): The info used to compute the aggregate.

        Returns:
            str: the value of the aggregate.

    """
    return aggregate_getter.get_from_config(name, config_filepath, info)


def get_info_from_aggregate(config_filepath, aggregate, value):
    """Extract info from the given aggregate.

        Args:
            config_filepath (str): Path of the configuration file to consider.
            aggregate (str): Name of the aggregate to consider.
            value (dict(str, int)): Value of the aggregate in which extract info.

        Returns:
            dict(str, int): extracted info.

    """
    return info_getter.get_from_aggregate(config_filepath, aggregate, value)
