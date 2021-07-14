from typing import List
from tag_linter.rule import Rule
from .default import template_default


def template_helicopter(data) -> List[Rule]:
    parent = data.get('parent')
    add_children = data.get('add_children', [])

    # For the time being, we accept no other source
    children = add_children

    tags = [parent]

    tags.extend([('-' + i) for i in children])

    return template_default({
        'name': data.get('name', 'heli-parent ' + parent),
        'note': data.get('note', "the tag '" + parent + "' should accompany one or more of its children"),
        'search': tags,
        'disabled': data.get('disabled', False)
    })
