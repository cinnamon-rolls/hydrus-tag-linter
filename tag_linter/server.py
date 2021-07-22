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
        self.rules_by_name = load_rules(args.rules)

        self.rules_by_uid = {}
        for rule in self.rules_by_name.values():
            self.rules_by_uid[rule.get_uid()] = rule

        self.archive_enabled = not args.disable_archive
        self.inbox_enabled = not args.disable_inbox

        if not self.archive_enabled and not self.inbox_enabled:
            print("Warning: both archive and inbox were disabled, so searches will be empty (why did you do this?)")

        self.client = create_hydrus_client(args)

        self.api_verison = self.client.api_version()

        self.password = args.password

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

    def get_rules(self):
        return list(self.rules_by_name.values())

    def get_rule_by_name(self, rule_name):
        return self.rules_by_name.get(rule_name.strip().lower())

    def get_rule_by_uid(self, rule_uid):
        return self.rules_by_uid.get(rule_uid)

    def get_rule_names(self) -> T.List[str]:
        ret = list(self.rules_by_name.keys())
        ret.sort()
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
                'name': 'Hydrus API',
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
                    }]
            }
        ]

    def is_password_protected(self):
        return self.password is not None

    def check_password(self, input) -> bool:
        "Return True if there is no password or if the given password matches"
        return self.password is None or self.password == input


# The one and only server instance, please do not make more :)
# Use this magic line:
# from tag_linter.server import instance as server
instance = Server()


def accept_user_args(args):
    """Gives the user's command line arguments to a new server instance. Please
    please PLEASE only call this once."""
    global instance
    instance.accept_user_args(args)
