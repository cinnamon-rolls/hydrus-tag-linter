from flask import Flask
import os


def create_app(args, options: dict):

    app: Flask = Flask(__name__, static_folder=None)

    # If this were a 'real' app you wouldn't see this, but this is a DIY project
    # meant for just one person, and any security is a joke to begin with :)
    app.secret_key = os.urandom(24)

    from .blueprints import create_master_blueprint

    app.register_blueprint(create_master_blueprint(app, options))

    import tag_linter.server

    tag_linter.server.accept_user_args(args)

    return app
