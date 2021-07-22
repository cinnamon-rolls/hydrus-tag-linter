from typing import List
from tag_linter.rule import Rule
from .default import forward_to_default

COLOR_EXEMPT = [
    "-monochrome"
]

HAIR_COLOR_EXEMPT = []
HAIR_COLOR_EXEMPT.extend(COLOR_EXEMPT)

EYE_COLOR_EXEMPT = []
EYE_COLOR_EXEMPT.extend(COLOR_EXEMPT)


def rm_tag_action(tag):
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


def extract_tag(data, prefix, modifier=None):
    tag = data.get(prefix + " tag")

    if tag is not None and not isinstance(tag, str):
        raise ValueError("Not a string: '" + prefix + " tag'")

    if tag is None:
        tag = data.get(prefix)
        if tag is None:
            raise ValueError(
                "Not specified: '" + prefix + "' or '" + prefix + " tag'")
        if not isinstance(tag, str):
            raise ValueError("Not a string: '" + prefix + "'")
        if modifier is not None:
            tag = modifier(tag)

    if not isinstance(tag, str):
        raise ValueError("Not a string: " + str(tag))

    return tag


def extract_character_tag(data):
    return extract_tag(data, "character", lambda x: "character:" + x)


def template_character_hair_color(data, character_tag=None) -> List[Rule]:
    if character_tag is None:
        character_tag = extract_character_tag(data)

    good_tag = extract_tag(data, "hair color", lambda x: x + " hair")

    search = [character_tag]
    search.append("-" + good_tag)
    search.extend(HAIR_COLOR_EXEMPT)

    actions = [
        add_tag_action(good_tag),
        add_tag_action('monochrome'),
        rm_tag_action(character_tag)
    ]

    return forward_to_default(
        data,
        {
            'search': search,
            'actions': actions
        }, {
            'name': 'Hair Color: ' + character_tag,
            'note': "the tag '" + good_tag + "' should accompany '" + character_tag + "'",
        })


def template_character_eye_color(data, character_tag=None) -> List[Rule]:
    if character_tag is None:
        character_tag = extract_character_tag(data)

    good_tag = extract_tag(data, "eye color", lambda x: x + " eyes")

    search = [character_tag]
    search.append("-" + good_tag)
    search.extend(EYE_COLOR_EXEMPT)

    actions = [
        add_tag_action(good_tag),
        add_tag_action('monochrome'),
        rm_tag_action(character_tag)
    ]

    return forward_to_default(
        data,
        {
            'search': search,
            'actions': actions
        }, {
            'name': 'Eye Color: ' + character_tag,
            'note': "the tag '" + good_tag + "' should accompany '" + character_tag + "'",
        })


def template_character_traits_hub(data) -> List[Rule]:
    ret = []

    character_tag = extract_character_tag(data)

    hair_color = data.get('hair color')
    if isinstance(hair_color, dict):
        ret.extend(template_character_hair_color(hair_color, character_tag))

    eye_color = data.get('eye color')
    if isinstance(eye_color, dict):
        ret.extend(template_character_eye_color(eye_color, character_tag))

    return ret
