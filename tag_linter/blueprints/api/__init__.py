from tag_linter.hydrus_util import ids2hashes
from json.decoder import JSONDecodeError
from flask import Blueprint, jsonify, request, abort, make_response
from tag_linter.server import instance as server
import json
import tag_linter.searches
import tag_linter.actions

blueprint = Blueprint('api', __name__)


TAG_ACTION_ADD_LOCAL = "0"
TAG_ACTION_DELETE_LOCAL = "1"


def get_rule(rule_name):
    if rule_name is None:
        abort(400, "rule name not specified")
    rule = server.get_rule(rule_name)
    if rule is None:
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


@blueprint.route('/api/rules/get_rules', methods=['GET'])
def api_get_rules():
    ret = list(map(lambda x: x.as_dict(), server.get_rules()))
    return jsonify(ret)


@blueprint.route('/api/rules/get_rule/', methods=['GET'])
def api_get_rule():
    rule = get_rule(request.args.get('name'))
    return jsonify(rule.as_dict())


@blueprint.route('/api/rules/get_rule_names', methods=['GET'])
def api_get_rule_names():
    return jsonify(server.get_rule_names())


@blueprint.route('/api/rules/get_files', methods=['GET'])
def api_get_rule_files():
    rule = get_rule(request.args.get('name'))
    refresh = request.args.get('refresh', False)
    return jsonify(rule.get_files(refresh=refresh))


@blueprint.route('/api/rules/apply_linter_tag', methods=['GET'])
def api_rules_apply_linter_tag():
    preview = request.args.get('preview', 'true') == 'true'
    rule = get_rule(request.args.get('name'))
    tag_raw = request.args.get('tag', rule.get_linter_rule_tag())
    tag_service = server.tag_service

    enable_add = request.args.get('add', 'true') == 'true'
    enable_remove = request.args.get('remove', 'true') == 'true'

    tag = server.get_client().clean_tags([tag_raw])[0]

    files_tagged_now = server.search_by_tags(tags=[tag])
    files_that_need_tag = rule.get_files(refresh=True)

    files_to_untag = [
        i for i in files_tagged_now if i not in files_that_need_tag]

    files_to_tag = [
        i for i in files_that_need_tag if i not in files_tagged_now]

    if not preview:
        # Add
        if(len(files_to_tag) > 0) and enable_add:
            print('add...')
            server.get_client().add_tags(
                hashes=ids2hashes(files_to_tag),
                service_to_action_to_tags={
                    server.tag_service: {
                        TAG_ACTION_ADD_LOCAL: [tag]
                    }
                }
            )

        # Remove
        if(len(files_to_untag) > 0) and enable_remove:
            print('remove...')
            server.get_client().add_tags(
                hashes=ids2hashes(files_to_untag),
                service_to_action_to_tags={
                    server.tag_service: {
                        TAG_ACTION_DELETE_LOCAL: [tag]
                    }
                }
            )

    return jsonify({
        'preview': preview,
        'tag': tag,
        'added': len(files_to_tag),
        'removed': len(files_to_untag),
        'tag_service': tag_service
    })


@blueprint.route('/api/rules/get_actions', methods=['GET'])
def api_rules_get_actions():
    rule = get_rule(request.args.get('name'))
    return jsonify(rule.get_actions())


@blueprint.route('/api/server/get_global_file_actions', methods=['GET'])
def api_server_get_global_file_actions():
    return jsonify([i.as_dict() for i in tag_linter.actions.FILE_GLOBAL_ACTIONS])


@blueprint.route('/api/server/get_summary', methods=['GET'])
def api_server_get_summary():
    return jsonify(server.get_summary())


@blueprint.route('/api/file/get_metadata', methods=['GET'])
def api_file_get_metadata():
    return jsonify(server.get_file_metadata(request.args.get('file_id')))


@blueprint.route('/api/file/change_tags', methods=['GET'])
def api_file_add_tags():
    file_ids = coerce_list(parse_json_arg(request.args, 'file_ids'))
    add_tags = coerce_list(parse_json_arg(request.args, 'add_tags'))
    rm_tags = coerce_list(parse_json_arg(request.args, 'rm_tags'))

    hashes = ids2hashes(file_ids)

    if len(hashes) > 0 and (len(add_tags) > 0 or len(rm_tags) > 0):
        print(str(hashes))
        print(str(add_tags))
        print(str(rm_tags))
        server.get_client().add_tags(
            hashes=hashes,
            service_to_action_to_tags={
                server.tag_service: {
                    TAG_ACTION_ADD_LOCAL: add_tags,
                    TAG_ACTION_DELETE_LOCAL: rm_tags
                }
            }
        )

    return jsonify({})


@blueprint.route('/api/search/get_files', methods=['GET'])
def api_search_get_files():
    input_raw = request.args.get('search')
    try:
        input = json.loads(input_raw)
    except JSONDecodeError:
        abort(400, "invalid json: '" + input_raw + "'")
    search = tag_linter.searches.load_search(input)
    return jsonify(search.execute(server))


@blueprint.route('/api/hydrus/add_tags/clean_tags', methods=['GET'])
def api_hydrus_clean_tags():
    tags_input = request.args.get('tags')
    tags = json.loads(tags_input)
    return jsonify(server.client.clean_tags(tags))
