import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(args, options: dict):

    app: Flask = Flask(__name__, static_folder=None)

    # If this were a 'real' app you wouldn't see this, but this is a DIY project
    # meant for just one person, and any security is a joke to begin with :)
    app.secret_key = os.urandom(24)

    db_path = options.get("db_path")

    if not isinstance(db_path, str):
        raise ValueError("db_path is not a string")

    database_uri = "sqlite:////" + db_path

    print("database uri: " + database_uri)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = SQLAlchemy(app)

    db.create_all()

    from .blueprints import create_master_blueprint

    app.register_blueprint(create_master_blueprint(app, options))

    import tag_linter.server

    tag_linter.server.accept_user_args(args)

    return app
