#!/usr/bin/env python3

from flask.helpers import make_response
from tag_linter.server import instance as server
from flask import Flask, send_from_directory, render_template, session, redirect, abort, request
import sys
import json
import os

import tag_linter.blueprints.api
import tag_linter.blueprints.user

aggressive_static_caching = False

app: Flask = Flask(__name__, static_folder=None)

# If this were a 'real' app you wouldn't see this, but this is a DIY project
# meant for just one person, and any security is a joke to begin with :)
app.secret_key = os.urandom(24)

blueprint_api = tag_linter.blueprints.api.blueprint


@blueprint_api.before_request
def guard_api():
    if server.is_password_protected() and not session.get('logged_in', False):
        return abort(403)


app.register_blueprint(blueprint_api, url_prefix='/api')

blueprint_user = tag_linter.blueprints.user.blueprint


@blueprint_user.before_request
def guard_user():
    if server.is_password_protected() and not session.get('logged_in', False):
        return redirect("/login")


app.register_blueprint(blueprint_user, url_prefix='')


@app.route("/static/<path:path>")
def send_static_file(path):
    res = send_from_directory(os.path.join(app.root_path, 'static'), path)
    if not app.debug:
        res.headers.add('Cache-Control', 'public, max-age=3600, immutable')
    return res


@ app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


@ app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('logged_in', False):
            return redirect("/")
        return render_template('login.html')
    else:
        password = request.get_json(force=True).get('password')
        print(password)
        if server.check_password(password):
            session['logged_in'] = True
            return "OK"
        return abort(400, "wrong password")


@ app.before_first_request
def before_first_request():
    "set up globals here"
    tag_linter.server.accept_user_args(args)
    print("done with 'before first request'")


@ app.context_processor
def context_process():
    return {
        'len': len,
        'server': server,
        'json': json
    }


def main(args) -> int:
    global app, aggressive_static_caching

    run_kwargs = {
        'host': args.host,
        'port': args.port,
        'debug': args.debug
    }
    aggressive_static_caching = not args.debug

    if args.ssl_adhoc == True:
        run_kwargs['ssl_context'] = 'adhoc'
        print("NOTE: Running on an an adhoc certificate")

    app.run(**run_kwargs)

    return 0


if __name__ == "__main__":
    import tag_linter.arg_config as arg_config
    import tag_linter.server

    global args

    args = arg_config.parse_args()

    try:
        sys.exit(main(args))
    except KeyboardInterrupt:
        pass
