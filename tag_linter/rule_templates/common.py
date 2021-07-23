def rm_tag_action(tag):
    if not isinstance(tag, str):
        raise ValueError("not a string: '" + str(tag) + "'")

    return {
        'name': "Remove " + tag,
        'icon': 'tag_blue_delete',
        'archetype': 'change_tags',
        'shortcut': 'auto',
        'resolves': True,
        'hints': {
            'rm_tags': tag
        }
    }


def add_tag_action(tag):
    if not isinstance(tag, str):
        raise ValueError("not a string: '" + str(tag) + "'")

    return {
        'name': "Add " + tag,
        'icon': 'tag_blue_add',
        'archetype': 'change_tags',
        'shortcut': 'auto',
        'resolves': True,
        'hints': {
            'add_tags': tag
        }
    }
