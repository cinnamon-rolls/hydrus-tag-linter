from tag_linter.server import instance as server
from tag_linter.hydrus_util import ids2hashes
from tag_linter.actions import load_action


class Rule:
    def __init__(self, data: dict):
        from tag_linter.searches import load_search

        self.search = load_search(data.get('search'))
        self.name = data.get('name', 'Unnamed Rule')
        self.note = data.get('note', None)
        self.disabled = data.get('disabled', False)

        self.icon_active = data.get('icon_active')
        self.icon_disabled = data.get('icon_disabled')
        self.icon_done = data.get('icon_done', 'accept')

        self.actions = [load_action(i) for i in data.get('actions', [])]

    def get_info(self) -> dict:
        ret = {
            'name': self.name,
            'note': self.note,

            'icon_active': self.icon_active,
            'icon_disabled': self.icon_disabled,
            'icon_done': self.icon_done,

            'noncompliance_tag': self.get_noncompliance_tag(),
            'exempt_tag': self.get_exempt_tag()
        }
        if self.disabled:
            ret['disabled'] = True
        return ret

    def is_enabled(self):
        return not self.disabled

    def get_files(self):
        if(not self.is_enabled()):
            return []

        print("get_files: " + self.name)

        ret = self.search.execute(server)

        exempt = self.get_exempt_files()
        ret = [i for i in ret if i not in exempt]

        self.cached_files = ret
        return ret

    def get_exempt_files(self):
        return server.search_by_tags([self.get_exempt_tag()])

    def get_hashes(self):
        return ids2hashes(self.get_files())

    def get_hashes_as_str(self) -> str:
        text = "\n".join(self.get_hashes())
        return text

    def get_actions(self):
        return self.actions

    def get_name(self):
        return self.name if self.name is not None else "Unnamed Rule"

    def get_note(self):
        return self.note

    def has_note(self):
        return self.note is None

    def __repr__(self):
        return self.name

    def get_noncompliance_tag(self):
        """
        This is the tag to apply to files that are noncompliant with this rule,
        and to remove from files that are not
        """
        return "linter rule:" + self.get_name()

    def get_exempt_tag(self):
        return "linter exempt:" + self.get_name()
