from json.decoder import JSONDecodeError
import typing as T
from flask import abort
from tag_linter.rule import Rule
from tag_linter.server import instance as server
import json

TAG_ACTION_ADD_LOCAL = "0"
TAG_ACTION_DELETE_LOCAL = "1"


def get_rule(rule_name) -> Rule:
    if rule_name is None:
        abort(400, "rule name not specified")
    rule = server.get_rule(rule_name)
    if rule is None:
        print("no rule definition found for '" + rule_name + "'")
        abort(400, "rule not found: '" + rule_name + "'")
    return rule


def parse_json_arg(args: dict, arg_name: str, default_value: T.Any = None) -> T.Any:
    raw = args.get(arg_name)
    if raw is None:
        return default_value
    try:
        return json.loads(raw)
    except JSONDecodeError:
        abort(400, "bad json for '" + arg_name + "': " + raw)


def coerce_list(value):
    if value is None:
        return []
    if not isinstance(value, list):
        return [value]
    return value


def for_each_json_elem(jsons, func):
    try:
        elems = json.loads(jsons)
    except JSONDecodeError:
        return abort(400, "invalid json: '" + jsons + "'")
    return for_each_elem(elems, func)


def for_each_elem(elems, func):
    if isinstance(elems, list):
        return [func(i) for i in elems]
    else:
        return func(elems)
