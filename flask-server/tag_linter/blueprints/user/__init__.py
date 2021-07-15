from flask import Blueprint, abort, make_response
from tag_linter.server import instance as server
import requests
from flask import render_template, make_response, abort


blueprint = Blueprint('user', __name__)


@blueprint.route('/', methods=['GET'])
def app_get_index():
    server.refresh_all()
    return render_template('index.html')


@blueprint.route('/rules/<rule_name>', methods=['GET'])
def app_get_rule(rule_name):
    rule = server.get_rule(rule_name)
    if rule is None:
        abort(404, "Rule not found: '" + rule_name + "'")
    rule.get_files(refresh=True)
    return render_template('rule.html', rule=rule)


@blueprint.route('/file', methods=['GET'])
def app_get_file():
    return render_template('file.html')


@blueprint.route('/files/thumbnail/<file_id>', methods=['GET'])
def app_get_file_thumbnail(file_id):
    thumb_res: requests.Response = server.get_client().get_thumbnail(file_id=file_id)
    my_res = make_response(thumb_res.content)
    # just hope the browser can figure it out...
    # it should just be a jpg or png
    my_res.mimetype = 'image'
    return my_res


@blueprint.route('/files/full/<file_id>', methods=['GET'])
def app_get_file_full(file_id):
    metadata = server.get_file_metadata(file_id)
    file_res: requests.Response = server.get_client().get_file(file_id=file_id)
    my_res = make_response(file_res.content)
    my_res.mimetype = metadata.get('mime')
    return my_res


@blueprint.route('/search', methods=['GET'])
def app_search_by_tag():
    return render_template('search.html')