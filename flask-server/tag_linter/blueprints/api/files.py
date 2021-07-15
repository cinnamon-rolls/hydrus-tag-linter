from flask import Blueprint, jsonify, request, abort, make_response
from tag_linter.blueprints.api.common import *
from tag_linter.hydrus_util import *

blueprint = Blueprint('api files', __name__)


@blueprint.route('/get_metadata', methods=['GET'])
def api_file_get_metadata():
    return jsonify(server.get_file_metadata(request.args.get('file_id')))


@blueprint.route('/move_to_trash', methods=['POST'])
def api_file_move_to_trash():
    body = request.get_json(force=True)
    file_ids = coerce_list(body.get('file_ids'))
    delete_files(file_ids)
    return jsonify({})


@blueprint.route('/move_to_inbox', methods=['POST'])
def api_file_move_to_inbox():
    body = request.get_json(force=True)
    file_ids = coerce_list(body.get('file_ids'))
    undelete_files(file_ids)
    unarchive_files(file_ids)
    return jsonify({})


@blueprint.route('/move_to_archive', methods=['POST'])
def api_file_move_to_archive():
    body = request.get_json(force=True)
    file_ids = coerce_list(body.get('file_ids'))
    undelete_files(file_ids)
    archive_files(file_ids)
    return jsonify({})


@blueprint.route('/change_tags', methods=['POST'])
def api_file_add_tags():
    body = request.get_json(force=True)
    file_ids = coerce_list(body.get('file_ids'))
    add_tags = coerce_list(body.get('add_tags'))
    rm_tags = coerce_list(body.get('rm_tags'))

    hashes = ids2hashes(file_ids)
    # print(str(hashes))
    # print(str(add_tags))
    # print(str(rm_tags))

    if len(hashes) > 0 and (len(add_tags) > 0 or len(rm_tags) > 0):
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
