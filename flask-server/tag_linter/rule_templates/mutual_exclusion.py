from typing import List
from tag_linter.rule import Rule
from .default import template_default


def template_mutual_exclusion(data) -> List[Rule]:
    tags = data.get('tags')
    if tags is None or len(tags) < 2:
        return []

    if len(tags) > 2:
        raise ValueError('for now, only lists of length 2 are supported')

    defaultName = "mutual exclusion: " + ", ".join(tags)

    def create_only_action(tag):
        return {
            'name': "Only '" + tag + "'",
            'archetype': 'change_tags',
            'shortcut': 'auto',
            'resolves': True,
            'hints': {
                'add_tags': [tag],
                'rm_tags': [i for i in tags if i is not tag]
            }
        }

    actions = [create_only_action(i) for i in tags]

    actions.append({
        'name': "None (Remove all)",
        'archetype': 'change_tags',
        'shortcut': 'auto',
        'resolves': True,
        'hints': {
            'rm_tags': tags
        }
    })

    note = data.get('note', "The tags " + ", ".join(tags) +
                    " are mutually exclusive, so only one should be present")

    return template_default({
        'name': data.get('name', defaultName),
        'note': note,
        'search': tags,
        'actions': actions
    })
