class Action:
    def __init__(self, data: dict):
        self.name = data.get('name', 'Unnamed Action')
        self.icon = data.get('icon')
        self.archetype = data.get('archetype')
        self.hints = data.get('hints', {})
        self.hidden = data.get('hidden', False)

    def as_dict(self) -> dict:
        return {
            'name': self.name,
            'icon': self.icon,
            'archetype': self.archetype,
            'hints': self.hints,
            'hidden': self.hidden
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
        'icon': 'delete',
        'name': 'Move to Trash',
        'archetype': 'move_to_trash'
    })
]
