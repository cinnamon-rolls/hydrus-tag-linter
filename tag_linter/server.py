import tag_linter.rules
import typing
import hydrus

from tag_linter.rule import Rule
from typing import List, Iterable

NAME = "hydrus tag linter"
PERMISSIONS = [
    hydrus.Permission.SearchFiles,
    hydrus.Permission.AddTags
]


def get_key(args, permissions):
    "Gets the Hydrus Client API key supplied in the args, or read from input if its not specified"


def create_hydrus_client(args):
    import hydrus.utils

    if(args.api_key is not None):
        key = args.api_key
    else:
        key = hydrus.utils.cli_request_api_key(
            "hydrus tag linter", PERMISSIONS)

    if(not key):
        raise ValueError("The API key could not be obtained.")

    # Try to log in
    client = hydrus.Client(key, args.api_url)
    if not hydrus.utils.verify_permissions(client, PERMISSIONS):
        raise ValueError(
            "The API key does not grant all required permissions:",
            PERMISSIONS)

    return client

# https://stackoverflow.com/a/8290508


def batch(iterable: Iterable, batch_size: int = 256):
    """
    Breaks a large list into batches of a predetermined size
    """

    if isinstance(iterable, set):
        iterable = list(iterable)

    l = len(iterable)
    for ndx in range(0, l, batch_size):
        yield iterable[ndx:min(ndx + batch_size, l)]



class Server:
    def __init__(self, args):
        self.lint_rules = tag_linter.rules.load_rules(args.rules)

        self.archive_enabled = not args.disable_archive
        self.inbox_enabled = not args.disable_inbox
        self.tag_service = args.tag_service

        self.client = create_hydrus_client(args)

        self.api_verison = self.client.api_version()

    def is_archive_enabled(self):
        return self.archive_enabled

    def is_inbox_enabled(self):
        return self.inbox_enabled

    def search_by_tags(self, tags):
        if self.inbox_enabled and self.archive_enabled:
            # neither are disabled
            return self.client.search_files(tags)

        elif not self.inbox_enabled and not self.archive_enabled:
            # both were disabled :(
            print("Warning: both archive and inbox were disabled, so searches will be empty (why did you do this?)")
            return []

        else:
            # one or the other was disabled
            return self.get_client().search_files(self.tags, self.inbox_enabled, self.archive_enabled)

    def get_rules(self, sort_reverse=True) -> List[Rule]:
        ret = list(self.lint_rules.values())
        ret.sort(
            key=lambda a: len(self.get_rule_files(a)),
            reverse=sort_reverse
        )
        return ret

    def get_rule(self, rule_name: str) -> Rule:
        return self.lint_rules.get(rule_name)

    def get_rule_names(self) -> List[str]:
        return list(self.lint_rules.keys())

    def get_client(self) -> hydrus.BaseClient:
        return self.client

    def get_rule_files(self, rule: typing.Union[str, Rule], refresh=False):
        if isinstance(rule, str):
            rule = self.get_rule(rule)

        if rule is None:
            return None

        return rule.get_files(self.client, self.inbox_enabled, self.archive_enabled, refresh)

    def get_rule_hashes(self, rule: typing.Union[str, Rule], refresh=False):
        if isinstance(rule, str):
            rule = self.get_rule(rule)
        return self.ids2hashes(self.get_rule_files(rule=rule, refresh=refresh))

    def get_rule_hashes_as_str(self, rule: typing.Union[str, Rule], refresh=False) -> str:
        if isinstance(rule, str):
            rule = self.get_rule(rule)

        text = "\n".join(self.get_rule_hashes(rule=rule, refresh=refresh))
        return text

    def refresh_all(self):
        for rule in self.lint_rules.values():
            self.get_rule_files(rule=rule, refresh=True)

    def count_issues(self, refresh=False):
        ret = 0
        for rule in self.lint_rules.values():
            ret += len(self.get_rule_files(rule=rule, refresh=refresh))
        return ret

    def count_rules_without_issues(self, refresh=False):
        ret = 0
        for rule in self.lint_rules.values():
            if len(self.get_rule_files(rule=rule, refresh=refresh)) == 0:
                ret += 1
        return ret

    def ids2hashes(self, file_ids):
        ret = []
        batch_size = 256

        batches = batch(file_ids, batch_size)

        for search_batch in batches:
            res = self.client.file_metadata(file_ids=search_batch)
            for val in res:
                ret.append(val.get('hash'))

        return ret

    def get_summary(self) -> List[dict]:
        return [{
            'name': "Total issues",
            'value': self.count_issues()
        }, {
            'name': "Total rules",
            'value': len(self.get_rules())
        }, {
            'name': "Rules without issues",
            "value": self.count_rules_without_issues()
        }, {
            'name': "Inbox Enabled?",
            "value": self.inbox_enabled
        }, {
            'name': "Archive Enabled?",
            'value': self.archive_enabled
        }, {
            'name': "API Version",
            'value': self.api_verison
        }, {
            'name': "API URL",
            'value': self.client.api_url
        }, {
            'name': "Tag Service",
            'value': self.tag_service
        }]
