
class Configuration:
    def __init__(self, filepath=None, conf_data=None):
        conf_data = conf_data or dict()

        self.filepath = filepath
        self.name = conf_data.get("name", None)
        self.trees = conf_data.get("trees")
        self.scopes = conf_data.get("scopes", list())
        self.search_terms = conf_data.get("search_terms", dict())
        self.aggregates = conf_data.get("aggregates", dict())
        self.auto_arbo_required_info = conf_data.get("auto_arbo", list())

    @property
    def aggregates_names(self):
        return list(self.aggregates.keys())

    @staticmethod
    def is_valid_conf_data(conf_data):
        conditions = [
            isinstance(conf_data.get("name", str()), str),
            isinstance(conf_data.get("trees"), list),
            isinstance(conf_data.get("scopes", list()), list),
            isinstance(conf_data.get("search_terms", dict()), dict),
            isinstance(conf_data.get("aggregates", dict()), dict),
            isinstance(conf_data.get("auto_arbo", list()), list),
        ]
        return all(conditions) is True

    def extend_with_linked_data(self, linked_data):
        self.trees.extend(linked_data.get("trees"))
        for search_term, values in linked_data.get("search_terms", dict()).items():
            self.search_terms[search_term] = self.search_terms.get(search_term, list()) + values
        for aggregate, value in linked_data.get("aggregates", dict()).items():
            self.search_terms.setdefault(aggregate, value)
        self.scopes = list(set(self.scopes + linked_data.get("scopes", list())))
        self.auto_arbo_required_info = list(set(self.auto_arbo_required_info + linked_data.get("auto_arbo", list())))



