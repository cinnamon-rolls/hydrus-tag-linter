DEFAULT_ICONS_FOR_ARCHETYPE = {
    "quick_add_tag": "tag_blue_add",
    "quick_delete_tag": "tag_blue_delete",
    "move_to_trash": "bin_closed",
    "move_to_inbox": "email",
    "move_to_archive": "database_add",
    "change_tags": "tag_blue"
}


class Action:
    def __init__(self, data: dict):
        self.name = data.get("name", "Unnamed Action")
        self.icon = data.get("icon")
        self.archetype = data.get("archetype")
        self.hints = data.get("hints", {})
        self.shortcut = data.get("shortcut")

        self.hidden = data.get("hidden", False)
        self.hiddenIfInbox = data.get("hiddenIfInbox", False)
        self.hiddenIfArchive = data.get("hiddenIfArchive", False)
        self.hiddenIfTrash = data.get("hiddenIfTrash", False)

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "icon": self.get_icon(),
            "archetype": self.archetype,
            "hints": self.hints,
            "shortcut": self.shortcut,

            "hidden": self.hidden,
            "hiddenIfInbox": self.hiddenIfInbox,
            "hiddenIfArchive": self.hiddenIfArchive,
            "hiddenIfTrash": self.hiddenIfTrash
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
        "archetype": "quick_add_tag"
    }),
    Action({
        "name": "Quick Tag (Delete)",
        "archetype": "quick_delete_tag"
    }),
    Action({
        "name": "Move to Trash",
        "archetype": "move_to_trash",
        "hiddenIfTrash": True
    }),
    Action({
        "name": "Move to Inbox",
        "archetype": "move_to_inbox",
        "hiddenIfInbox": True
    }),
    Action({
        "name": "Move to Archive",
        "archetype": "move_to_archive",
        "hiddenIfArchive": True
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
