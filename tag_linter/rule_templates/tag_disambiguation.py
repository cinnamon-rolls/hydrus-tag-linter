from typing import List
from tag_linter.rule import Rule
from .default import forward_to_default


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

    def create_replace_action(tag):
        return {
            'name': tag,
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
        'name': "Other...",
        'archetype': 'quick_add_tag',
        'shortcut': 'auto',
        'resolves': True,
        'hints': {
            'rm_tags': bad_tag
        }
    })

    actions.append({
        'name': "None",
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

    return forward_to_default(
        data,
        {
            'search': search,
            'actions': actions
        }, {
            'name': "disambiguation: " + bad_tag_str,
            'note': "The tag(s) " + bad_tag_str + " has/have fallen out of favor, and should be replaced with one of: " + ", ".join(alternatives) + ", or otherwise removed",
        })
