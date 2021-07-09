import typing
import hydrus
import hydrus.utils
from tag_linter.rules import Rule, load_rules
from typing import List

NAME = "hydrus tag linter"
PERMISSIONS = [
    hydrus.Permission.SearchFiles
]


def get_key(args, permissions):
    "Gets the Hydrus Client API key supplied in the args, or read from input if its not specified"
    if(args.api_key is not None):
        return args.api_key
    else:
        return hydrus.utils.cli_request_api_key("hydrus tag linter", permissions)


def create_hydrus_client(args):
    # Get the key
    key = str(get_key(args, PERMISSIONS))
    if(not key):
        raise ValueError("The API key could not be obtained.")

    # Try to log in
    client = hydrus.Client(key, args.api_url)
    if not hydrus.utils.verify_permissions(client, PERMISSIONS):
        raise ValueError(
            "The API key does not grant all required permissions:",
            PERMISSIONS)

    return client


class Server:
    def __init__(self, args):
        self.lint_rules = load_rules(args.rules)

        self.archive_enabled = not args.disable_archive
        self.inbox_enabled = not args.disable_inbox

        self.client = create_hydrus_client(args)

        self.api_verison = self.client.api_version()

    def is_archive_enabled(self):
        return self.archive_enabled

    def is_inbox_enabled(self):
        return self.inbox_enabled

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

        if rule is None:
            return None

        return rule.get_hashes(self.client, self.inbox_enabled, self.archive_enabled, refresh=refresh)

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
        }]
