import typing as T
import tag_linter.hydrus_util as hydrus_util


class Server:
    def __init__(self):
        print("Server: __init__")

    def accept_user_args(self, args):
        from tag_linter.rules import load_rules
        self.rules_by_name = load_rules(args.rules)

        self.rules_by_uid = {}
        for rule in self.rules_by_name.values():
            self.rules_by_uid[rule.get_uid()] = rule

        self.archive_enabled = not args.disable_archive
        self.inbox_enabled = not args.disable_inbox

        if not self.archive_enabled and not self.inbox_enabled:
            print("Warning: both archive and inbox were disabled")

    def search_by_tags(self, tags):
        return hydrus_util.search_by_tags(tags, self.inbox_enabled, self.archive_enabled)

    def is_archive_enabled(self) -> bool:
        return self.archive_enabled

    def is_inbox_enabled(self) -> bool:
        return self.inbox_enabled

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


# The one and only server instance, please do not make more :)
# Use this magic line:
# from tag_linter.server import instance as server
instance = Server()


def accept_user_args(args):
    """Gives the user's command line arguments to a new server instance. Please
    please PLEASE only call this once."""
    global instance
    instance.accept_user_args(args)
