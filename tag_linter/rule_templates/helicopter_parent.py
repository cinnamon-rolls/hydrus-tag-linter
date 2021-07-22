from typing import List
from tag_linter.rule import Rule
from .default import forward_to_default


def template_helicopter(data) -> List[Rule]:
    parent = data.get('parent')
    add_children = data.get('add_children', [])

    # For the time being, we accept no other source
    children = add_children

    search = [parent]

    search.extend([('-' + i) for i in children])

    return forward_to_default(
        data,
        {
            'search': search,
        }, {
            'name': 'heli-parent ' + parent,
            'note': "the tag '" + parent + "' should accompany one or more of its children",
        })
