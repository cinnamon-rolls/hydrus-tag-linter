DEFAULT_ICONS_FOR_ARCHETYPE = {
    "quick_add_tag": "tag_blue_add",
    "quick_delete_tag": "tag_blue_delete",
    "move_to_trash": "bin_closed",
    "move_to_inbox": "email",
    "move_to_archive": "database_add",
    "change_tags": "tag_blue",
    "mark_as_exempt": "asterisk_yellow",
    "unmark_as_exempt": "asterisk_yellow",
    "skip": "arrow_right"
}


class Action:
    def __init__(self, data: dict):
        self.name = data.get("name", "Unnamed Action")
        self.icon = data.get("icon")
        self.archetype = data.get("archetype")
        self.hints = data.get("hints", {})
        self.shortcut = data.get("shortcut")
        self.resolves = data.get("resolves")

        self.hidden = data.get("hidden", False)
        self.hiddenIfInbox = data.get("hiddenIfInbox", False)
        self.hiddenIfArchive = data.get("hiddenIfArchive", False)
        self.hiddenIfTrash = data.get("hiddenIfTrash", False)
        self.hiddenIfRule = data.get("hiddenIfRule", False)
        self.hiddenIfNoRule = data.get("hiddenIfNoRule", False)
        self.hiddenIfExempt = data.get("hiddenIfExempt", False)
        self.hiddenIfNotExempt = data.get("hiddenIfNotExempt", False)

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "icon": self.get_icon(),
            "archetype": self.archetype,
            "hints": self.hints,
            "shortcut": self.shortcut,
            "resolves": self.resolves,

            "hidden": self.hidden,
            "hiddenIfInbox": self.hiddenIfInbox,
            "hiddenIfArchive": self.hiddenIfArchive,
            "hiddenIfTrash": self.hiddenIfTrash,
            "hiddenIfRule": self.hiddenIfRule,
            "hiddenIfNoRule": self.hiddenIfNoRule,
            "hiddenIfExempt": self.hiddenIfExempt,
            "hiddenIfNotExempt": self.hiddenIfNotExempt
        }

    def get_icon(self):
        if self.icon is not None:
            return self.icon
        else:
            return DEFAULT_ICONS_FOR_ARCHETYPE.get(self.archetype)


def load_action(data):
    if not isinstance(data, dict):
        raise ValueError("expected a dict, but got " + str(data))
    return Action(data)


FILE_GLOBAL_ACTIONS = [
    Action({
        "name": "Quick Tag (Add)",
        "archetype": "quick_add_tag",
        "shortcut": "="
    }),
    Action({
        "name": "Quick Tag (Delete)",
        "archetype": "quick_delete_tag",
        "shortcut": "-"
    }),
    Action({
        "name": "Move to Trash",
        "archetype": "move_to_trash",
        "hiddenIfTrash": True,
        "shortcut": "d"
    }),
    Action({
        "name": "Move to Inbox",
        "archetype": "move_to_inbox",
        "hiddenIfInbox": True,
        "shortcut": "shift+a"
    }),
    Action({
        "name": "Move to Archive",
        "archetype": "move_to_archive",
        "hiddenIfArchive": True,
        "shortcut": "a"
    }),
    Action({
        "name": "Mark as Exempt",
        "archetype": "mark_as_exempt",
        "shortcut": "x",
        "resolves": True,
        "hiddenIfNoRule": True,
        "hiddenIfExempt": True
    }),
    Action({
        "name": "Remove Exemption",
        "archetype": "unmark_as_exempt",
        "shortcut": "shift+x",
        "hiddenIfNoRule": True,
        "hiddenIfNotExempt": True
    }),
    Action({
        "name": "Skip",
        "archetype": "skip",
        "shortcut": "s",
        "resolves": True,
        "hiddenIfNoRule": True
    }),
    Action({
        "name": "Move Right",
        "archetype": "move",
        "hidden": True,
        "shortcut": "arrowright",
        "hints": {
            "movement": 1
        }
    }),
    Action({
        "name": "Move Left",
        "archetype": "move",
        "hidden": True,
        "shortcut": "arrowleft",
        "hints": {
            "movement": -1
        }
    })
]
