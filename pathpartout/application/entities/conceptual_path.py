import re


class ConceptualPath:
    def __init__(self, path_elements):
        self.path_elements = path_elements or list()

    @staticmethod
    def get_all_empty_info(conceptual_paths):
        info = set()
        for path in conceptual_paths:
            path.parse_info_names(info)
        return {i: None for i in info}

    def parse_info_names(self, info):
        for element in self.path_elements:
            variable_pattern = re.compile("\{\{([\w]+)\??:?[\w]*\}\}")  # {{variable_name[?:number]}}
            info.update(variable_pattern.findall(element))

    def extract(self, concrete_filepath):
        concrete_filepath = concrete_filepath.replace('\\', '/')
        concrete_filepath_elements = concrete_filepath.split('/')

        if len(concrete_filepath_elements) != len(self.path_elements):
            raise ValueError("Given filepath doesn't match the label path in the config file.")

        info = dict()
        for i, element in enumerate(concrete_filepath_elements):
            self.extract_from_path_element(element, self.path_elements[i], info)
        return info

    def extract_from_path_element(self, concrete_element, conceptual_element, info):
        variable_pattern = re.compile("\{\{([\w]+)(\?)?:?([\w]+)?\}\}")  # {{variable_name[?:number]}}
        variable_found = variable_pattern.findall(conceptual_element)

        re_element = conceptual_element
        for var in variable_found:
            occurrence = "{" + var[2] + "}" if var[2] else "*" if var[1] else "+"
            re_element = variable_pattern.sub("([A-Za-z0-9_]" + occurrence + ")", re_element, count=1)

        element_pattern = re.compile(re_element)
        match = element_pattern.fullmatch(concrete_element)
        if not match:
            raise ValueError("Given filepath doesn't match the label path in the config file.")

        for i, var in enumerate(variable_found):
            info[var[0]] = match.group(i+1)

    def fill(self, info):
        variable_pattern = re.compile("\{\{([\w]+)\??:?[\w]*\}\}")  # {{variable_name[?:number]}}

        concept_path = "/".join(self.path_elements)
        variables_found = variable_pattern.findall(concept_path)
        missing_variables = set([var for var in variables_found if not info.get(var)])
        if missing_variables:
            raise ValueError(f"Missing info to found label path : {','.join(missing_variables)}")

        path = concept_path
        for var in variables_found:
            path = variable_pattern.sub(info.get(var), path, count=1)
        return path










