from json.decoder import JSONDecodeError
from flask import abort
from tag_linter.server import instance as server
import json

TAG_ACTION_ADD_LOCAL = "0"
TAG_ACTION_DELETE_LOCAL = "1"


def get_rule(rule_name):
    if rule_name is None:
        abort(400, "rule name not specified")
    rule = server.get_rule(rule_name)
    if rule is None:
        print("no rule definition found for '" + rule_name + "'")
        abort(400, "rule not found: '" + rule_name + "'")
    return rule


def parse_json_arg(args, arg_name):
    raw = args.get(arg_name)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except JSONDecodeError:
        abort("bad json for '" + arg_name + "': " + raw)


def coerce_list(value):
    if value is None:
        return []
    if not isinstance(value, list):
        return [value]
    return value
