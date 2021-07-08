from tag_linter.searches import load_search

from typing import Union, Iterable, Dict, List
import json
import os
import hydrus

JSON_EXT = ".json"


# https://stackoverflow.com/a/8290508
def batch(iterable, batch_size=256):
    """
    Breaks a
    """

    if isinstance(iterable, set):
        iterable = list(iterable)

    l = len(iterable)
    for ndx in range(0, l, batch_size):
        yield iterable[ndx:min(ndx + batch_size, l)]


def ids2hashes(client: hydrus.BaseClient, file_ids):
    ret = []
    batch_size = 256

    batches = batch(file_ids, batch_size)

    for search_batch in batches:
        res = client.file_metadata(file_ids=search_batch)
        for val in res:
            ret.append(val.get('hash'))

    return ret


class Rule:
    def __init__(self, data: dict):
        self.search = load_search(data.get('search'))
        self.name = data.get('name', 'Unnamed Rule')
        self.note = data.get('note', None)
        self.disabled = data.get('disabled', False)
        self.cached_files = None

    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'note': self.note
        }

    def is_enabled(self):
        return not self.disabled

    def get_files(self, client, inbox, archive, refresh : bool = False):
        if(not self.is_enabled()):
            return []

        if refresh == True:
            self.cached_files = None

        if self.cached_files is not None:
            return self.cached_files

        print("get files: " + self.name)

        ret = self.search.execute(client, inbox, archive)
        self.cached_files = ret
        return ret

    def get_hashes(self, client, inbox, archive, refresh=False):
        return ids2hashes(client, self.get_files(client=client, inbox=inbox, archive=archive, refresh=refresh))

    def get_name(self):
        return self.name if self.name is not None else "Unnamed Rule"

    def get_note(self):
        return self.note

    def has_note(self):
        return self.note is None

    def __repr__(self):
        return self.name


def load_rule_from_data(data : Union[None, Dict, List]) -> List[Rule]:
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
        return [Rule(data=data)]

    raise ValueError('Unsure how to parse Rule from type ' + str(type(data)) + ", see: " + str(data))


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


def load_rules_from_dirs(rules_dirs : Union[str, List[str]]) -> List[Rule]:
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

            if not os.path.isdir(subfile) and subfile.endswith(JSON_EXT):
                ret.extend(load_rules_from_file(subfile_name))

            else:
                ret.extend(load_rules_from_dirs(subfile_name))

    return ret

def load_rules(paths : Union[str, Iterable[str]]) -> Dict[str, Rule]:
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