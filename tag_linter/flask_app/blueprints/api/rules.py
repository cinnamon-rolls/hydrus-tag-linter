from flask import Blueprint, jsonify, request, abort, make_response
from .common import *
from tag_linter.hydrus_util import *

blueprint = Blueprint('api rules', __name__)


@blueprint.route('/get_rule_names', methods=['GET'])
def api_get_rule_names():
    return jsonify(server.get_rule_names())


@blueprint.route('/get_info', methods=['GET'])
def api_get_rule():
    get_all = parse_json_arg(request.args, 'all', False)
    include_file_count = parse_json_arg(
        request.args, 'include_file_count', False)
    include_exemption_count = parse_json_arg(
        request.args, 'include_exemption_count', False)

    if get_all:
        elems = server.get_rule_names()
    else:
        elems = parse_json_arg(request.args, 'names')

    def conversion(ruleName):
        rule = get_rule(ruleName)
        info = rule.get_info()

        if include_file_count:
            info['file_count'] = rule.count_files()

        if include_exemption_count:
            info['exemption_count'] = rule.count_exempt_files()

        return info

    return jsonify(for_each_elem(elems, conversion))


@blueprint.route('/get_actions', methods=['GET'])
def api_rules_get_actions():
    rule = get_rule(request.args.get('name'))
    return jsonify([i.as_dict() for i in rule.get_actions()])


@blueprint.route('/get_files', methods=['GET'])
def api_get_rule_files():
    rule = get_rule(request.args.get('name'))
    return jsonify(rule.get_files())


@blueprint.route('/get_files_count', methods=['GET'])
def api_get_rule_files_count():
    return jsonify(get_rule(request.args.get('name')).count_files())


@blueprint.route('/get_exemptions', methods=['GET'])
def api_get_rule_exemptions():
    return jsonify(get_rule(request.args.get('name')).get_exempt_files())


@blueprint.route('/get_exemptions_count', methods=['GET'])
def api_get_rule_exemptions_count():
    return jsonify(get_rule(request.args.get('name')).count_exempt_files())


@blueprint.route('/apply_noncompliance_tag', methods=['GET'])
def api_rules_apply_noncompliance_tag():
    preview = request.args.get('preview', 'true') == 'true'
    rule = get_rule(request.args.get('name'))
    tag_raw = request.args.get('tag', rule.get_noncompliance_tag())
    tag_service = request.args.get('tag_service', 'my tags')

    enable_add = request.args.get('add', 'true') == 'true'
    enable_remove = request.args.get('remove', 'true') == 'true'

    tag = server.get_client().clean_tags([tag_raw])[0]

    files_tagged_now = server.search_by_tags(tags=[tag])
    files_that_need_tag = rule.get_files()

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
                    tag_service: {
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
                    tag_service: {
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
