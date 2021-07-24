from flask import (
    session,
    redirect,
    abort,
    Blueprint,
    send_from_directory,
    render_template,
    request,
)

from tag_linter.server import instance as server


import os


def create_master_blueprint(app, db_models, options):
    blueprint = Blueprint("master_blueprint", __name__)

    from .api import create_blueprint as create_api_blueprint
    from .user import blueprint as blueprint_user

    blueprint_api = create_api_blueprint(app, db_models, options)

    @blueprint_api.before_request
    def guard_api():
        if server.is_password_protected() and not session.get(
                "logged_in", False):
            return abort(403)

    @blueprint_user.before_request
    def guard_user():
        if server.is_password_protected() and not session.get(
                "logged_in", False):
            return redirect("/login")

    blueprint.register_blueprint(blueprint_api, url_prefix="/api")
    blueprint.register_blueprint(blueprint_user, url_prefix="")

    @blueprint.route("/static/<path:path>")
    def send_static_file(path):
        res = send_from_directory(os.path.join(app.root_path, "static"), path)
        if options.get("aggressive_static_caching", False):
            res.headers.add("Cache-Control", "public, max-age=3600, immutable")
        return res

    @blueprint.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    @blueprint.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            if session.get("logged_in", False):
                return redirect("/")
            return render_template("login.html")
        else:
            password = request.get_json(force=True).get("password")
            print(password)
            if server.check_password(password):
                session["logged_in"] = True
                return "OK"
            return abort(400, "wrong password")

    return blueprint
