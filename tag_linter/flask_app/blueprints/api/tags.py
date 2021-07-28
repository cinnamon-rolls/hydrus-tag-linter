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

    @blueprint.route("/transpose_namespace")
    def transpose_namespace():
        inbox = parse_json_arg(request.args, 'inbox', False)
        archive = parse_json_arg(request.args, 'archive', False)
        tag_service = request.args.get('tag_service')

        from_namespace = request.args.get('from_namespace')
        to_namespace = request.args.get('to_namespace')
        suffix = request.args.get('suffix')
        prefix = request.args.get('prefix')

        as_string = parse_json_arg(request.args, 'as_string', False)

        changes = hydrus_util.transpose_namespace(
            from_namespace=from_namespace,
            to_namespace=to_namespace,
            prefix=prefix,
            suffix=suffix,
            inbox=inbox,
            archive=archive,
            tag_service=tag_service)

        if as_string:
            ret = ""
            for bad_tag in changes.keys():
                good_tag = changes.get(bad_tag)
                ret += bad_tag + "\n" + good_tag + "\n"
            return plaintext_response(ret)
        else:
            return jsonify(changes)


    return blueprint
