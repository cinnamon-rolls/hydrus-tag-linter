from tag_linter.searches import load_search

from typing import Iterable, Dict, List
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

    def get_uid(self):
        return self.uid


def load_rules_from_file(rule_file_name: str) -> List[Rule]:
    "Reads a rule and returns it, or returns None if the rule is otherwise disabled"

    print("Reading rule file: " + rule_file_name)
    with open(rule_file_name) as rule_file:
        data = json.load(rule_file)


    if isinstance(data, list):
        ret = [Rule(data=i) for i in data]
    else:
        ret = [Rule(data=data)]

    return ret


def load_rules_from_dirs(rules_dirs) -> Dict[str, Rule]:
    if not isinstance(rules_dirs, Iterable):
        rules_dirs = [rules_dirs]

    ret = {}

    for rule_dir in rules_dirs:
        for file in os.listdir(rule_dir):
            if file.endswith(JSON_EXT):
                rules = load_rules_from_file(rule_dir + '/' + file)
                for rule in rules:
                    if rule is not None and rule.is_enabled():
                        ret[rule.get_name()] = rule

    return ret
