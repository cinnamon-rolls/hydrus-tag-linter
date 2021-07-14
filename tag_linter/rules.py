from tag_linter.rule import Rule

from typing import Any, Union, Iterable, Dict, List
import json
import os

JSON_EXT = ".json"


def construct_one(data) -> Rule:
    """
    Defines the 'default' way to construct a Rule. Note that other templates may
    defer to this template, or invoke this method many times.
    """
    return Rule(data)


def template_default(data) -> List[Rule]:
    return [construct_one(data)]


def template_helicopter(data) -> List[Rule]:
    parent = data.get('parent')
    add_children = data.get('add_children', [])

    # For the time being, we accept no other source
    children = add_children

    tags = [parent]

    tags.extend([('-' + i) for i in children])

    return construct_one({
        'name': data.get('name', 'heli-parent ' + parent),
        'note': data.get('note', "the tag '" + parent + "' should accompany one or more of its children"),
        'search': tags,
        'disabled': data.get('disabled', False)
    })


def template_mutual_exclusion(data) -> List[Rule]:
    tags = data.get('tags')
    if tags is None or len(tags) < 2:
        return []

    if len(tags) > 2:
        raise ValueError('for now, only lists of length 2 are supported')

    defaultName = "mutual exclusion: " + ", ".join(tags)

    def create_only_action(tag):
        return {
            'name': "Only '" + tag + "'",
            'archetype': 'change_tags',
            'shortcut': 'auto',
            'resolves': True,
            'hints': {
                'add_tags': [tag],
                'rm_tags': [i for i in tags if i is not tag]
            }
        }

    actions = [create_only_action(i) for i in tags]

    actions.append({
        'name': "None (Remove all)",
        'archetype': 'change_tags',
        'shortcut': 'auto',
        'resolves': True,
        'hints': {
            'rm_tags': tags
        }
    })

    return template_default({
        'name': data.get('name', defaultName),
        'note': "The tags " + ", ".join(tags) + " are mutually exclusive, so only one should be present",
        'search': tags,
        'actions': actions
    })


templates = {
    'default': template_default,
    'helicopter parent': template_helicopter,
    'mutual exclusion': template_mutual_exclusion
}


def apply_template(data: dict, template_name: Union[str, None] = None) -> List[Rule]:

    if template_name is None:
        template_name = data.get('template', 'default')

    template = templates.get(template_name.strip().lower(), template_default)

    return template(data)


def load_rules_from_data(data: Union[None, Dict, List]) -> List[Rule]:
    """
    Reads a rule from a some object (likely obtained from an already parsed JSON
    document), and returns all of the rules that could be parsed from it.
    """

    if data is None:
        return []

    if isinstance(data, list):
        ret = []
        for i in data:
            ret.extend(load_rules_from_data(i))
        return ret

    if isinstance(data, dict):
        ret = apply_template(data=data)
        if not isinstance(ret, Iterable):
            ret = [ret]
        return ret

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

    return load_rules_from_data(data=data)


def load_rules_from_dirs(rules_dirs: Union[str, List[str]]) -> List[Rule]:
    """
    Recursively searches through a directory for Rule files, parses them, and
    returns all parsed rules as a flat list
    Assumes that the paths provided are indeed existing directories
    """

    if not isinstance(rules_dirs, list):
        rules_dirs = [rules_dirs]

    ret = []

    for rule_dir in rules_dirs:

        print("Searching directory: " + rule_dir)

        for subfile in os.listdir(rule_dir):

            subfile_name = rule_dir + "/" + subfile

            if os.path.isdir(subfile_name):
                ret.extend(load_rules_from_dirs(subfile_name))

            elif subfile.endswith(JSON_EXT):
                ret.extend(load_rules_from_file(subfile_name))

            else:
                print("Ignoring: " + subfile_name)

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

        print(rules)
        for rule in rules:
            ret[rule.get_name().strip().lower()] = rule

    return ret
