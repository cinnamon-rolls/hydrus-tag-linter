from flask import Blueprint, jsonify, request, abort
from tag_linter.server import instance as server
from tag_linter.hydrus_util import get_services
import json
import tag_linter.searches
import tag_linter.actions
from .common import *


def create_blueprint(app, db_models, options):
    blueprint = Blueprint('soft_parents', __name__)

    SoftParentRelation = db_models.SoftParentRelation

    @blueprint.route("/add", methods=['GET', 'POST'])
    def add():
        children = coerce_list(parse_json_arg(request.args, 'children', []))
        parents = coerce_list(parse_json_arg(request.args, 'parents', []))
        for child in children:
            for parent in parents:
                SoftParentRelation.ensure(child, parent)
        return jsonify({})

    @blueprint.route("/remove", methods=['GET', 'POST'])
    def remove():
        children = coerce_list(parse_json_arg(request.args, 'children', []))
        parents = coerce_list(parse_json_arg(request.args, 'parents', []))
        for child in children:
            for parent in parents:
                SoftParentRelation.remove(child, parent)
        return jsonify({})

    return blueprint
