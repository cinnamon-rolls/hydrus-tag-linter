#!/usr/bin/env python3

from tag_linter.server import instance as server
import requests
from flask import Flask, render_template, make_response, send_from_directory
import sys
import json
import os

import tag_linter.blueprints.api

app = Flask(__name__)

app.register_blueprint(tag_linter.blueprints.api.blueprint)


def extract_tags_from_metadata(metadata: dict):
    sntstdt = dict.get('service_names_to_statuses_to_display_tags', {})
    stdt = sntstdt.get(server.tag_service, {})
    display_tags = stdt.get('0', {})
    return display_tags


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET'])
def app_get_index():
    server.refresh_all()
    return render_template('index.html')


@app.route('/rules/<rule_name>', methods=['GET'])
def app_get_rule(rule_name):
    rule = server.get_rule(rule_name)
    rule.get_files(refresh=True)
    return render_template('rule.html', rule=rule)


@app.route('/file', methods=['GET'])
def app_get_file():
    return render_template('file.html')


@app.route('/files/thumbnail/<file_id>', methods=['GET'])
def app_get_file_thumbnail(file_id):
    thumb_res: requests.Response = server.get_client().get_thumbnail(file_id=file_id)
    my_res = make_response(thumb_res.content)
    # just hope the browser can figure it out...
    # it should just be a jpg or png
    my_res.mimetype = 'image'
    return my_res


@app.route('/files/full/<file_id>', methods=['GET'])
def app_get_file_full(file_id):
    metadata = server.get_file_metadata(file_id)
    file_res: requests.Response = server.get_client().get_file(file_id=file_id)
    my_res = make_response(file_res.content)
    my_res.mimetype = metadata.get('mime')
    return my_res


@app.route('/search', methods=['GET'])
def app_search_by_tag():
    return render_template('search.html')


@app.before_first_request
def before_first_request():
    "set up globals here"
    tag_linter.server.accept_user_args(args)
    print("done with 'before first request'")


@app.context_processor
def context_process():
    return {
        'len': len,
        'server': server,
        'json': json
    }


def main(args) -> int:
    global app

    app.run(host=args.host,
            port=args.port,
            debug=args.debug)

    return 0


if __name__ == "__main__":
    import tag_linter.arg_config as arg_config
    import tag_linter.server

    global args

    argp = arg_config.get_argp()
    args = argp.parse_args()

    try:
        sys.exit(main(args))
    except KeyboardInterrupt:
        pass
