from flask import Blueprint, jsonify, request, abort
from tag_linter.server import instance as server
from tag_linter.hydrus_util import get_services
import json
import tag_linter.searches
import tag_linter.actions
from .common import *


def create_blueprint(app, db_models, options):
    blueprint = Blueprint('api tags', __name__)

    @blueprint.route("/search_and_destroy")
    def search_and_destroy():
        tags = coerce_list(parse_json_arg(request.args, 'tags', []))

        inbox = parse_json_arg(request.args, 'inbox', False)
        archive = parse_json_arg(request.args, 'archive', False)

        files_audited = 0

        return jsonify({
            'files_audited': files_audited
        })

    return blueprint
