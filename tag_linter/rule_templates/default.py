from typing import List
from tag_linter.rule import Rule


def template_default(data) -> List[Rule]:
    """
    Defines the 'default' way to construct a Rule. Note that other templates may
    defer to this template, or invoke this method many times.
    """
    return [Rule(data)]
