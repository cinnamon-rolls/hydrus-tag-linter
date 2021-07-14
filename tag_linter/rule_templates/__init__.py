from typing import List, Union
from tag_linter.rule import Rule

from .helicopter_parent import template_helicopter
from .mutual_exclusion import template_mutual_exclusion
from .default import template_default
from .tag_disambiguation import template_tag_disambiguation


templates = {
    'default': template_default,
    'helicopter parent': template_helicopter,
    'mutual exclusion': template_mutual_exclusion,
    'tag disambiguation': template_tag_disambiguation
}


def apply_template(data: dict, template_name: Union[str, None] = None) -> List[Rule]:

    if template_name is None:
        template_name = data.get('template', 'default')

    template = templates.get(template_name.strip().lower())

    if(template is None):
        raise ValueError("cannot find template: " + template_name)

    return template(data)
