from json.decoder import JSONDecodeError
from flask import Blueprint, jsonify, request, abort
from tag_linter.server import instance as server
from tag_linter.hydrus_util import get_services
import json
import tag_linter.searches
import tag_linter.actions
from .common import *
from .files import blueprint as api_files
from .rules import blueprint as api_rules

blueprint = Blueprint('api', __name__)


blueprint.register_blueprint(api_files, url_prefix='files')
blueprint.register_blueprint(api_rules, url_prefix='rules')


@blueprint.route('/server/get_global_file_actions', methods=['GET'])
def api_server_get_global_file_actions():
    return jsonify([i.as_dict() for i in tag_linter.actions.FILE_GLOBAL_ACTIONS])


@blueprint.route('/server/get_info', methods=['GET'])
def api_server_get_info():
    return jsonify(server.get_info())


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


@blueprint.route("/services/get_services", methods=['GET'])
def api_services_get_services():
    return jsonify(get_services())
