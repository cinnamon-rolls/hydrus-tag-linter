from typing import List
from tag_linter.rule import Rule
from .default import forward_to_default
from .common import *


def template_soft_parent(data) -> List[Rule]:
    parents = data.get('parents')
    children = data.get('children')

    if isinstance(parents, str):
        parents = [parents]
    if isinstance(children, str):
        children = [children]

    ret = []

    for parent in parents:
        search = [i for i in children]
        search.append("-" + parent)

        actions = [
            add_tag_action(parent)
        ]

        rule = forward_to_default(
            data,
            {
                'search': search,
                'actions': actions
            }, {
                'note': "The tag '" + parent + "' is generally seen around these other tags..."
            })

        ret.extend(rule)

    return ret
