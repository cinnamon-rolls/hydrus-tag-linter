from tag_linter.hydrus_util import ids2hashes
from json.decoder import JSONDecodeError
from flask import Blueprint, jsonify, request, abort, make_response
from tag_linter.server import instance as server
from tag_linter.blueprints.api.common import *
import json
import tag_linter.searches
import tag_linter.actions
import tag_linter.blueprints.api.files as api_files

blueprint = Blueprint('api', __name__)


blueprint.register_blueprint(api_files.blueprint, url_prefix='files')


@blueprint.route('/rules/get_rules', methods=['GET'])
def api_get_rules():
    ret = list(map(lambda x: x.as_dict(), server.get_rules()))
    return jsonify(ret)


@blueprint.route('/rules/get_rule/', methods=['GET'])
def api_get_rule():
    rule = get_rule(request.args.get('name'))
    return jsonify(rule.as_dict())


@blueprint.route('/rules/get_rule_names', methods=['GET'])
def api_get_rule_names():
    return jsonify(server.get_rule_names())


@blueprint.route('/rules/get_files', methods=['GET'])
def api_get_rule_files():
    rule = get_rule(request.args.get('name'))
    refresh = request.args.get('refresh', False)
    return jsonify(rule.get_files(refresh=refresh))


@blueprint.route('/rules/get_exemptions', methods=['GET'])
def api_get_rule_exemptions():
    rule = get_rule(request.args.get('name'))
    return jsonify(rule.get_exempt_files())


@blueprint.route('/rules/apply_noncompliance_tag', methods=['GET'])
def api_rules_apply_noncompliance_tag():
    preview = request.args.get('preview', 'true') == 'true'
    rule = get_rule(request.args.get('name'))
    tag_raw = request.args.get('tag', rule.get_noncompliance_tag())
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


@blueprint.route('/rules/get_actions', methods=['GET'])
def api_rules_get_actions():
    rule = get_rule(request.args.get('name'))
    return jsonify(rule.get_actions())


@blueprint.route('/server/get_global_file_actions', methods=['GET'])
def api_server_get_global_file_actions():
    return jsonify([i.as_dict() for i in tag_linter.actions.FILE_GLOBAL_ACTIONS])


@blueprint.route('/server/get_summary', methods=['GET'])
def api_server_get_summary():
    return jsonify(server.get_summary())


@blueprint.route('/search/get_files', methods=['GET'])
def api_search_get_files():
    input_raw = request.args.get('search')
    try:
        input = json.loads(input_raw)
    except JSONDecodeError:
        abort(400, "invalid json: '" + input_raw + "'")
    search = tag_linter.searches.load_search(input)
    return jsonify(search.execute(server))


@blueprint.route('/tags/clean_tags', methods=['GET'])
def api_hydrus_clean_tags():
    tags_input = request.args.get('tags')
    tags = json.loads(tags_input)
    return jsonify(server.client.clean_tags(tags))
