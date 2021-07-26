from flask import Blueprint, jsonify, request, abort, make_response
from .common import *
from tag_linter.hydrus_util import *

blueprint = Blueprint("api files", __name__)


@blueprint.route("/get_metadata", methods=["GET"])
def api_file_get_metadata():
    return jsonify(get_file_metadata(request.args.get("file_id")))


@blueprint.route("/move_to_trash", methods=["POST"])
def api_file_move_to_trash():
    body = request.get_json(force=True)
    file_ids = coerce_list(body.get("file_ids"))
    delete_files(file_ids)
    return jsonify({})


@blueprint.route("/move_to_inbox", methods=["POST"])
def api_file_move_to_inbox():
    body = request.get_json(force=True)
    file_ids = coerce_list(body.get("file_ids"))
    print("Move to inbox: " + str(file_ids))
    undelete_files(file_ids)
    unarchive_files(file_ids)
    return jsonify({})


@blueprint.route("/move_to_archive", methods=["POST"])
def api_file_move_to_archive():
    body = request.get_json(force=True)
    file_ids = coerce_list(body.get("file_ids"))
    print("Move to archive: " + str(file_ids))
    undelete_files(file_ids)
    archive_files(file_ids)
    return jsonify({})


@blueprint.route("/change_tags", methods=["POST"])
def api_file_add_tags():
    body = request.get_json(force=True)

    tag_service = body.get("tag_service")
    file_ids = coerce_list(body.get("file_ids"))
    add_tags = coerce_list(body.get("add_tags"))
    rm_tags = coerce_list(body.get("rm_tags"))

    change_tags(
        file_ids=file_ids,
        add_tags=add_tags,
        rm_tags=rm_tags,
        tag_service=tag_service)

    return jsonify({})
