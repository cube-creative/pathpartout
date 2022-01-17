import re


class ConceptualPath:
    parse_info_regex = re.compile("\{\{([\w]+)\??:?[\w]*\}\}") # {{variable_name[?:number]}}
    extract_regex = re.compile("\{\{([\w]+)(\?)?:?([0-9]*)(d)?\}\}")  # {{variable_name[?][:number][d]}}
    fill_regex = re.compile("\{\{([\w]+)(\?)?:?([0-9]*)(d)?\}\}")  # {{variable_name[?][:number][d]}}

    def __init__(self, path_elements):
        self.path_elements = path_elements or list()

    @staticmethod
    def get_all_empty_info(conceptual_paths):
        info = set()
        for path in conceptual_paths:
            info.update(path.parse_info_names())
        return {i: None for i in info}

    def parse_info_names(self):
        info = set()
        for element in self.path_elements:
            info.update(self.parse_info_regex.findall(element))
        return info

    def extract(self, concrete_filepath):
        concrete_filepath = concrete_filepath.replace('\\', '/')
        concrete_filepath_elements = concrete_filepath.split('/')

        if len(concrete_filepath_elements) != len(self.path_elements):
            raise ValueError("Path Partout: Given filepath doesn't match the label path in the config file.")

        info = dict()
        for i, element in enumerate(concrete_filepath_elements):
            self.extract_from_path_element(element, self.path_elements[i], info)
        return info

    def extract_from_path_element(self, concrete_element, conceptual_element, info):
        variable_found = self.extract_regex.findall(conceptual_element)
        re_element = conceptual_element
        for var in variable_found:
            occurrence = "{" + var[2] + "}" if var[2] else "*" if var[1] else "+"
            re_element = self.extract_regex.sub("([A-Za-z0-9_]" + occurrence + ")", re_element, count=1)

        element_pattern = re.compile(re_element)
        match = element_pattern.fullmatch(concrete_element)
        if not match:
            raise ValueError(
                "Path Partout: Given filepath doesn't match the label path in the config file."
                "\n\tconcrete_element: {} doesn't match conceptual element: {}".format(concrete_element,
                                                                                       conceptual_element)
            )

        for i, var in enumerate(variable_found):
            is_number = var[3]
            new_info = match.group(i+1)
            info[var[0]] = new_info if not is_number else int(new_info)

    def fill(self, info):
        concept_path = "/".join(self.path_elements)
        variables_found = self.fill_regex.findall(concept_path)
        missing_variables = set([var[0] for var in variables_found if not info.get(var[0])])
        if missing_variables:
            raise ValueError(f"Path Partout: Missing info to found label path : {','.join(missing_variables)}")

        path = concept_path
        for var in variables_found:
            value = info.get(var[0])
            if var[2]:
                value = f"{value:0{var[1]}d}"
            path = self.fill_regex.sub(value, path, count=1)
        return path

    def contains_info_needed(self, info):
        info_needed_names = self.parse_info_names()
        for info_name in info_needed_names:
            if info.get(info_name) is None:
                return False
        return True
