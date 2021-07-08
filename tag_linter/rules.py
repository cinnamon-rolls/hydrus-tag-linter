from tag_linter.rule import Rule

from typing import Any, Union, Iterable, Dict, List
import json
import os

JSON_EXT = ".json"

AUTO_NOTE = " (This rule was automatically generated from a template.)"


def construct_one(data) -> Rule:
    """
    Defines the 'default' way to construct a Rule. Note that other templates may
    defer to this template, or invoke this method many times.
    """
    return Rule(data)


def template_default(data) -> List[Rule]:
    return [construct_one(data)]


templates = {
    'default': template_default,
}


def apply_template(data: dict, template_name: Union[str, None] = None) -> List[Rule]:

    if template_name is None:
        template_name = data.get('template', 'default')

    template = templates.get(template_name.strip().lower(), template_default)

    return template(data)


def load_rule_from_data(data: Union[None, Dict, List]) -> List[Rule]:
    """
    Reads a rule from a some object (likely obtained from an already parsed JSON
    document), and returns all of the rules that could be parsed from it.
    """

    if data is None:
        return []

    if isinstance(data, list):
        ret = []
        for i in data:
            ret.extend(load_rule_from_data(i))
        return ret

    if isinstance(data, dict):
        return apply_template(data=data)

    raise ValueError(
        'Unsure how to parse Rule from type ' +
        str(type(data)) + ", see: " + str(data))


def load_rules_from_file(rule_file_name: str) -> List[Rule]:
    """
    Reads a file and returns a list of rules that were parsed from that file
    Assumes that the file provided is indeed an existing file
    """

    print("Reading rule file: " + rule_file_name)

    if not os.path.isfile(rule_file_name):
        print("DOES NOT EXIST: " + rule_file_name)
        return None

    with open(rule_file_name) as rule_file:
        data = json.load(rule_file)

    return load_rule_from_data(data=data)


def load_rules_from_dirs(rules_dirs: Union[str, List[str]]) -> List[Rule]:
    """
    Recursively searches through a directory for Rule files, parses them, and
    returns all parsed rules as a flat list
    Assumes that the paths provided are indeed existing directories
    """

    if not isinstance(rules_dirs, list):
        rules_dirs = [rules_dirs]

    ret = []

    for rule_file in rules_dirs:

        print("Searching directory: " + rule_file)

        for subfile in os.listdir(rule_file):

            subfile_name = rule_file + "/" + subfile

            if not os.path.isdir(subfile):
                if subfile.endswith(JSON_EXT):
                    ret.extend(load_rules_from_file(subfile_name))

            else:
                ret.extend(load_rules_from_dirs(subfile_name))

    return ret


def load_rules(paths: Union[str, Iterable[str]]) -> Dict[str, Rule]:
    """
    It doesn't matter what the paths are (directories or files), this function
    will figure it out and delegate to other functions as needed
    """

    print("Loading rules...")

    ret = {}

    if not isinstance(paths, Iterable):
        paths = [paths]

    for path in paths:

        if not os.path.exists(path):
            print("DOES NOT EXIST: " + path)
            continue

        if os.path.isdir(path):
            rules = load_rules_from_dirs(path)
        else:
            rules = load_rules_from_file(path)

        for rule in rules:
            ret[rule.get_name()] = rule

    return ret
