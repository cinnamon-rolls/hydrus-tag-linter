from flask import Blueprint, jsonify, request, abort
import tag_linter.hydrus_util as hydrus_util
from .common import *


def create_blueprint(app, db_models, options):
    blueprint = Blueprint('api tags', __name__)

    @blueprint.route("/search_and_destroy")
    def search_and_destroy():
        inbox = parse_json_arg(request.args, 'inbox', False)
        archive = parse_json_arg(request.args, 'archive', False)
        read_tag_service = request.args.get('read_tag_service')
        write_tag_service = request.args.get('write_tag_service')

        tags = coerce_list(parse_json_arg(request.args, 'tags', []))

        removals = hydrus_util.search_and_destroy(
            tags=tags,
            inbox=inbox,
            archive=archive,
            read_tag_service=read_tag_service,
            write_tag_service=write_tag_service)

        return jsonify({"removals": removals})

    return blueprint
