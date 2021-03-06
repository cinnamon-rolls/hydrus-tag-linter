from json.decoder import JSONDecodeError
import typing as T
from flask import abort, make_response
from tag_linter.rule import Rule
from tag_linter.server import instance as server
import json


def get_rule(rule_name) -> Rule:
    if rule_name is None:
        abort(400, "rule name not specified")
    rule = server.get_rule_by_name(rule_name)
    if rule is None:
        rule = server.get_rule_by_uid(rule_name)
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


def plaintext_response(text):
    response = make_response(text, 200)
    response.mimetype = "text/plain; charset=utf-8"
    return response
