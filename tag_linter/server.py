import typing
import hydrus

import typing as T

NAME = "hydrus tag linter"
PERMISSIONS = [
    hydrus.Permission.SearchFiles,
    hydrus.Permission.AddTags
]


def create_hydrus_client(args) -> hydrus.BaseClient:
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


class Server:
    def __init__(self):
        print("Server: __init__")

    def accept_user_args(self, args):
        """Please do not call this unless you are in server.py, and you probably
        aren't in server.py"""
        from tag_linter.rules import load_rules
        self.rules = load_rules(args.rules)

        self.archive_enabled = not args.disable_archive
        self.inbox_enabled = not args.disable_inbox

        if not self.archive_enabled and not self.inbox_enabled:
            print("Warning: both archive and inbox were disabled, so searches will be empty (why did you do this?)")

        self.tag_service = args.tag_service

        self.client = create_hydrus_client(args)

        self.api_verison = self.client.api_version()

    def get_client(self) -> hydrus.BaseClient:
        return self.client

    def is_archive_enabled(self) -> bool:
        return self.archive_enabled

    def is_inbox_enabled(self) -> bool:
        return self.inbox_enabled

    def search_by_tags(self, tags):
        if self.inbox_enabled and self.archive_enabled:
            # neither are disabled
            return self.get_client().search_files(tags)
        elif not self.inbox_enabled and not self.archive_enabled:
            # both were disabled :(
            return []
        else:
            # one or the other was disabled
            return self.get_client().search_files(tags, self.inbox_enabled, self.archive_enabled)

    def get_rules(self, sort_reverse=True):
        ret = list(self.rules.values())

        def keyFunc(a):
            fs = a.get_files()
            if fs is None:
                raise ValueError("Rule '" + str(a) + "' returns None")
            return len(fs)

        ret.sort(
            key=keyFunc,
            reverse=sort_reverse
        )
        return ret

    def get_rule(self, rule_name):
        from tag_linter.rule import Rule
        if isinstance(rule_name, Rule):
            return rule_name
        return self.rules.get(rule_name.strip().lower())

    def get_rule_names(self) -> T.List[str]:
        return list(self.rules.keys())

    def refresh_all(self):
        for rule in self.rules.values():
            rule.get_files(refresh=True)

    def count_issues(self, refresh=False):
        ret = 0
        for rule in self.rules.values():
            ret += len(rule.get_files(refresh=refresh))
        return ret

    def count_rules_without_issues(self, refresh=False):
        ret = 0
        for rule in self.rules.values():
            if len(rule.get_files(refresh=refresh)) == 0:
                ret += 1
        return ret

    def get_file_metadata(self, file_id: T.Union[T.List[int], int]) -> hydrus.FileMetadataResultType:
        if file_id is None:
            raise ValueError('file_id is None')

        if isinstance(file_id, str):
            file_id = int(file_id)

        if isinstance(file_id, int):
            return self.get_client().file_metadata(file_ids=[file_id])[0]

        if isinstance(file_id, list):
            return self.get_client().file_metadata(file_ids=file_id)

        raise ValueError('unexpected input: ' + str(file_id))

    def get_summary(self) -> T.List[dict]:
        return [
            {
                'name': 'Progress',
                "value": [
                    {
                        'name': "Total issues",
                        'value': self.count_issues()
                    }, {
                        'name': "Total rules",
                        'value': len(self.get_rules())
                    }, {
                        'name': "Rules without issues",
                        "value": self.count_rules_without_issues()
                    }],
            }, {
                'name': 'Hydrus',
                "value": [
                    {
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
            }
        ]


# The one and only server instance, please do not make more :)
# Use this magic line:
# from tag_linter.server import instance as server
instance = Server()


def accept_user_args(args):
    """Gives the user's command line arguments to a new server instance. Please
    please PLEASE only call this once."""
    global instance
    instance.accept_user_args(args)
