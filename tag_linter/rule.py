from tag_linter.server import instance as server
from tag_linter.hydrus_util import ids2hashes


class Rule:
    def __init__(self, data: dict):
        from tag_linter.searches import load_search

        self.search = load_search(data.get('search'))
        self.name = data.get('name', 'Unnamed Rule')
        self.note = data.get('note', None)
        self.disabled = data.get('disabled', False)
        self.cached_files = None

        self.icon_active = data.get('icon_active')
        self.icon_disabled = data.get('icon_disabled')
        self.icon_done = data.get('icon_done', 'accept')

    def as_dict(self) -> dict:
        ret = {
            'search': self.search.as_jsonifiable(),
            'name': self.name,
            'note': self.note
        }
        if self.disabled:
            ret['disabled'] = True
        return ret

    def is_enabled(self):
        return not self.disabled

    def get_files(self, refresh: bool = False):
        if(not self.is_enabled()):
            return []

        if refresh == True:
            self.cached_files = None
        elif self.cached_files is not None:
            return self.cached_files

        print("get_files: " + self.name)

        ret = self.search.execute(server)
        self.cached_files = ret
        return ret

    def get_hashes(self, refresh=False):
        return ids2hashes(self.get_files(refresh=refresh))

    def get_hashes_as_str(self, refresh=False) -> str:
        text = "\n".join(self.get_hashes(refresh=refresh))
        return text

    def get_icon(self, refresh=False):
        if not self.is_enabled():
            return self.icon_disabled
        if len(self.get_files(refresh=refresh)) > 0:
            return self.icon_active
        else:
            return self.icon_done

    def get_name(self):
        return self.name if self.name is not None else "Unnamed Rule"

    def get_note(self):
        return self.note

    def has_note(self):
        return self.note is None

    def __repr__(self):
        return self.name

    def get_linter_rule_tag(self):
        """
        This is the tag to apply to files that are noncompliant with this rule,
        and to remove from files that are not
        """
        return "linter rule:" + self.get_name()
