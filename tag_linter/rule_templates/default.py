from typing import List
from tag_linter.rule import Rule


def template_default(data) -> List[Rule]:
    """
    Defines the 'default' way to construct a Rule. Note that other templates may
    defer to this template, or invoke this method many times.
    """
    return [Rule(data)]


def forward_to_default(raw: dict, overrides: dict, fallbacks: dict) -> List[Rule]:
    actualData = raw.copy()

    if overrides is not None:
        for key in overrides.keys():
            actualData[key] = overrides[key]

    if fallbacks is not None:
        for key in fallbacks.keys():
            if actualData.get(key) is None:
                actualData[key] = fallbacks[key]

    return template_default(actualData)
