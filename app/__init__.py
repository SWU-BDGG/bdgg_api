from os import path
from os import mkdir

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import test_config
from app.secret_key import SECRET_KEY


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
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    __import__("app.models")
    db.init_app(app)
    migrate.init_app(app, db)

    from . import views
    for view in views.__all__:
        app.register_blueprint(blueprint=getattr(getattr(views, view), "bp"))

    return app
