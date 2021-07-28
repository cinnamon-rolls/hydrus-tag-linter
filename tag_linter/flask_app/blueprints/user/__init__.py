import tag_linter.hydrus_util as hydrus_util
from flask import Blueprint, abort, make_response, request
from tag_linter.server import instance as server
import requests
from flask import render_template, make_response, abort


blueprint = Blueprint('user', __name__)


@blueprint.route('/', methods=['GET'])
def app_get_index():
    return render_template('index.html')


@blueprint.route('/rule', methods=['GET'])
def app_get_rule():
    return render_template('rule.html')


@blueprint.route('/file', methods=['GET'])
def app_get_file():
    return render_template('file.html')


@blueprint.route('/files/thumbnail/<file_id>', methods=['GET'])
def app_get_file_thumbnail(file_id):
    thumb_res: requests.Response = hydrus_util.get_client().get_thumbnail(file_id=file_id)
    my_res = make_response(thumb_res.content)
    # just hope the browser can figure it out...
    # it should just be a jpg or png
    my_res.mimetype = 'image'
    my_res.headers.add('Cache-Control', 'public, max-age=604800, immutable')
    return my_res


@blueprint.route('/files/full/<file_id>', methods=['GET'])
def app_get_file_full(file_id):
    metadata = hydrus_util.get_file_metadata(file_id)
    file_res: requests.Response = hydrus_util.get_client().get_file(file_id=file_id)
    my_res = make_response(file_res.content)
    my_res.mimetype = metadata.get('mime')
    my_res.headers.add('Cache-Control', 'public, max-age=604800, immutable')
    return my_res


@blueprint.route('/search', methods=['GET'])
def app_search_by_tag():
    return render_template('search.html')


@blueprint.route('/soft_parents', methods=['GET'])
def app_soft_parents():
    return render_template('soft_parents.html')

@blueprint.route('/junk_tags', methods=['GET'])
def app_junk_tags():
    return render_template('junk_tags.html')

@blueprint.route('/search_and_destroy', methods=['GET'])
def app_search_and_destroy():
    return render_template('search_and_destroy.html')

@blueprint.route('/transpose_namespace', methods=['GET'])
def app_tranpose_namespace():
    return render_template('transpose_namespace.html')

@blueprint.route('/tools', methods=['GET'])
def app_tag_management():
    return render_template('tools.html')

