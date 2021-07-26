from flask import Blueprint, jsonify, request, abort
from .common import *
import tag_linter.hydrus_util as hydrus_util


def create_blueprint(app, db_models, options):
    blueprint = Blueprint('junk_tags', __name__)

    JunkTag = db_models.JunkTag

    @blueprint.route("/add", methods=['GET', 'POST'])
    def add():
        tags = coerce_list(parse_json_arg(request.args, 'tags', []))
        for tag in tags:
            JunkTag.ensure(tag)
        return jsonify({})

    @blueprint.route("/remove", methods=['GET', 'POST'])
    def remove():
        tags = coerce_list(parse_json_arg(request.args, 'tags', []))
        for tag in tags:
            JunkTag.remove(tag)
        return jsonify({})

    @blueprint.route("/count", methods=['GET', 'POST'])
    def count():
        return jsonify({
            "total": JunkTag.count()
        })

    @blueprint.route("/export", methods=['GET', 'POST'])
    def export():
        as_string = parse_json_arg(request.args, 'as_string', False)

        arr = JunkTag.export()

        if as_string:
            return plaintext_response("\n".join(arr))

        return jsonify({
            "junk_tags": arr
        })

    @blueprint.route("/search_and_destroy", methods=['GET', 'POST'])
    def search_and_destroy():
        inbox = parse_json_arg(request.args, 'inbox', False)
        archive = parse_json_arg(request.args, 'archive', False)
        read_tag_service = request.args.get('read_tag_service')
        write_tag_service = request.args.get('write_tag_service')

        tags = JunkTag.export()

        return jsonify(hydrus_util.search_and_destroy(
            tags=tags,
            inbox=inbox,
            archive=archive,
            read_tag_service=read_tag_service,
            write_tag_service=write_tag_service))

    return blueprint
