class Action:
    def __init__(self, data: dict):
        self.name = data.get('name', 'Unnamed Action')
        self.icon = data.get('icon')
        self.archetype = data.get('archetype')
        self.hints = data.get('hints', {})
        self.shortcut = data.get('shortcut')

        self.hidden = data.get('hidden', False)
        self.hiddenIfInbox = data.get('hiddenIfInbox', False)
        self.hiddenIfArchive = data.get('hiddenIfArchive', False)

    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'icon': self.icon,
            'archetype': self.archetype,
            'hints': self.hints,
            'shortcut': self.shortcut,

            'hidden': self.hidden,
            'hiddenIfInbox': self.hiddenIfInbox,
            'hiddenIfArchive': self.hiddenIfArchive
        }


def load_action(data):
    if not isinstance(data, dict):
        raise ValueError('expected a dict, but got ' + str(data))
    return Action(data)


FILE_GLOBAL_ACTIONS = [
    Action({
        'icon': 'tag_blue_add',
        'name': 'Quick Tag (Add)',
        'archetype': 'quick_add_tag'
    }),
    Action({
        'icon': 'tag_blue_delete',
        'name': 'Quick Tag (Delete)',
        'archetype': 'quick_delete_tag'
    }),
    Action({
        'icon': 'bin_closed',
        'name': 'Move to Trash',
        'archetype': 'move_to_trash'
    }),
    Action({
        'icon': 'email',
        'name': 'Move to Inbox',
        'archetype': 'move_to_inbox',
        'hiddenIfInbox': True
    }),
    Action({
        'icon': 'database_add',
        'name': 'Move to Archive',
        'archetype': 'move_to_archive',
        'hiddenIfArchive': True
    })
]
