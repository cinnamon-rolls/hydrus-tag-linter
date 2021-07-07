from searches import load_search

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

    def is_enabled(self):
        return not self.disabled

    def get_files(self, client, inbox, archive):
        return self.search.execute(client, inbox, archive)
    
    def get_hashes(self, client, inbox, archive):
        return ids2hashes(client, self.get_files(client, inbox, archive))


def load_rule(rule_file_name):
    "Reads a rule and returns it, or returns None if the rule is otherwise disabled"
    json_len = len(JSON_EXT)

    print("Reading: " + rule_file_name)
    with open(rule_file_name) as rule_file:
        data = json.load(rule_file)

    return Rule(data)


def load_rules(rules_dir):
    ret = []
    for file in os.listdir(rules_dir):
        if file.endswith(JSON_EXT):
            rule = load_rule(rules_dir + '/' + file)
            if rule is not None and rule.is_enabled():
                ret.append(rule)
    return ret
