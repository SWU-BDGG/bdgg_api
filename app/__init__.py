from os import path
from os import mkdir

from flask import Flask
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import test_config
from app.secret_key import SECRET_KEY
from app.database import get_url


db = SQLAlchemy()
migrate = Migrate()

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
UPLOAD_DIR = path.join(BASE_DIR, "app", "upload")


def test_upload_path():
    if not path.isdir(UPLOAD_DIR):
        mkdir(UPLOAD_DIR)


def create_app():
    test_upload_path()
    test_config()

    # >_<
    app = Flask(__name__)

    # session SECRET_KEY!
    app.config['SECRET_KEY'] = SECRET_KEY

    # sqlite for dev
    app.config['SQLALCHEMY_DATABASE_URI'] = get_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    __import__("app.models")
    db.init_app(app)
    migrate.init_app(app, db)

    from . import views
    for view in views.__all__:
        app.register_blueprint(blueprint=getattr(getattr(views, view), "bp"))

    @app.before_request
    def check_database_and_login():
        if app.config['SQLALCHEMY_DATABASE_URI'] == "#":
            if not request.path.startswith("/static") and not request.path.startswith("/setup"):
                return redirect(url_for("setup.step1"))
        else:
            if "user" not in session.keys():
                if not request.path.startswith("/api") and not request.path.startswith("/user/login"):
                    return redirect(url_for("user.login"))

    return app
