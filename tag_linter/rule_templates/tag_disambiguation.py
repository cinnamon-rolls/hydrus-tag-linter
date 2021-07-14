from typing import List
from tag_linter.rule import Rule
from .default import template_default


def template_tag_disambiguation(data) -> List[Rule]:
    bad_tag = data.get('bad_tag')
    alternatives = data.get('alternatives')

    if isinstance(bad_tag, str):
        bad_tag_str = bad_tag
    elif isinstance(bad_tag, list):
        if len(bad_tag) < 1:
            return []
        elif(len(bad_tag) == 1):
            bad_tag_str = str(bad_tag[0])
        else:
            bad_tag_str = bad_tag[0] + ", " + bad_tag[1]
            if len(bad_tag) > 2:
                bad_tag_str += " et al"
    else:
        raise ValueError("Bad value for bad_tag: " + str(bad_tag))

    default_name = "disambiguation: " + bad_tag_str

    def create_replace_action(tag):
        return {
            'name': "Replace with '" + tag + "'",
            'archetype': 'change_tags',
            'shortcut': 'auto',
            'resolves': True,
            'hints': {
                'add_tags': tag,
                'rm_tags': bad_tag
            }
        }

    actions = [create_replace_action(i) for i in alternatives]

    actions.append({
        'name': "Just remove the bad tag(s)",
        'archetype': 'change_tags',
        'shortcut': 'auto',
        'resolves': True,
        'hints': {
            'rm_tags': bad_tag
        }
    })

    if isinstance(bad_tag, list):
        search = {
            "op": "union",
            "of": bad_tag
        }
    else:
        search = bad_tag

    return template_default({
        'name': data.get('name', default_name),
        'note': "The tag(s) " + bad_tag_str + " has/have fallen out of favor, and should be replaced with one of: " + ", ".join(alternatives) + ", or otherwise removed",
        'search': search,
        'actions': actions
    })
