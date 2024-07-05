import os
from pathlib import Path
import re


def _get_platform_roots():
    """ Get the platform roots from the environment variable PATH_PARTOUT_ROOTS

    Returns:
        list: list of dictionnary with root label and path else None
    """ 
    plateform_roots = os.environ.get('PATH_PARTOUT_ROOTS', None)
    if not plateform_roots:
        return None
    plaform_roots_regex = re.compile("(?P<label>[^=&]+)=(?P<path>[^=&]+)")
    
    return {match.groupdict().get('label'):match.groupdict().get('path') for match in plaform_roots_regex.finditer(plateform_roots)}


class ConceptualPath:
    parse_info_regex = re.compile("\{\{([\w-]+)\??:?[\w]*\}\}") # {{variable_name[?:number]}}
    extract_regex = re.compile("\{\{([\w-]+)(\?)?:?([0-9]*)(d)?\}\}")  # {{variable_name[?][:number][d]}}
    fill_regex = re.compile("\{\{([\w-]+)(\?)?:?([0-9]*)(d)?\}\}")  # {{variable_name[?][:number][d]}}

    def __init__(self, path_elements: list):
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
        # concrete_filepath = concrete_filepath.replace('\\', '/')
        concrete_filepath_elements = [*Path(concrete_filepath).parts]
    
        if len(concrete_filepath_elements) != len(self.path_elements):
            raise ValueError(f"Path Partout: Given filepath doesn't match the label path in the config file. {concrete_filepath_elements} vs {self.path_elements}")

        info = dict()
        for i, element in enumerate(concrete_filepath_elements):
            self.extract_from_path_element(element, self.path_elements[i], info)
        return info

    def extract_from_path_element(self, concrete_element, conceptual_element, info):
        variable_found = self.extract_regex.findall(conceptual_element)
        re_element = conceptual_element
        for var in variable_found:
            occurrence = "{" + var[2] + "}" if var[2] else "*" if var[1] else "+"
            re_element = self.extract_regex.sub("([A-Za-z0-9_-]" + occurrence + ")", re_element, count=1)

        element_pattern = re.compile("(?:" + re_element.replace('\\','') + r")\Z")
        match = element_pattern.match(concrete_element.replace('\\',''))
        if match is None:
            raise ValueError(
                "Path Partout: Given filepath doesn't match the label path in the config file."
                "\n\tconcrete_element: {} doesn't match conceptual element: {}".format(concrete_element,
                                                                                       conceptual_element)
            )

        for i, var in enumerate(variable_found):
            is_number = var[3]
            new_info = match.group(i+1)
            info[var[0]] = new_info if not is_number else int(new_info)

    def fill(self, info, config_filepath):
        concept_path = Path(self.path_elements[0]).joinpath('/'.join(self.path_elements[1:])).as_posix()
        variables_found = self.fill_regex.findall(concept_path)
        missing_variables = set()
        for var in variables_found:
            info_name = var[0]
            facultative = var[1]
            if info.get(info_name) or facultative:
                continue
            missing_variables.add(info_name)

        if missing_variables:
            raise ValueError("Path Partout: Missing info to found label path : {missing_variables} \n"
                             "  Path: {concept_path} \n"
                             "  Config Path : {config_filepath}".format(
                                missing_variables=', '.join(missing_variables),
                                concept_path=concept_path,
                                config_filepath=config_filepath
                                )
                             )

        path = concept_path
        for var in variables_found:
            info_name = var[0]
            length = var[2]
            is_int = var[3]
            value = info.get(info_name)
            if is_int:
                value = str(value).zfill(int(length))
            path = self.fill_regex.sub(value, path, count=1)
        return path

    def contains_info_needed(self, info):
        info_needed_names = self.parse_info_names()
        for info_name in info_needed_names:
            if info.get(info_name) is None:
                return False
        return True
