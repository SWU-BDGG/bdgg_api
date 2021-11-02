from os import path
from os import mkdir

from flask import Flask
from flask import g
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

    app.config['SQLALCHEMY_DATABASE_URI'] = get_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    __import__("app.models")
    db.init_app(app)
    migrate.init_app(app, db)

    from . import views
    for view in views.__all__:
        app.register_blueprint(blueprint=getattr(getattr(views, view), "bp"))

    from . import template_filter
    for filter_name in template_filter.filter_list:
        app.add_template_filter(f=getattr(template_filter, filter_name), name=filter_name)

    @app.before_request
    def check_database_and_login():
        if app.config['SQLALCHEMY_DATABASE_URI'] == "#":
            flags = [
                x for x in [
                    "/static",
                    "/setup",
                ] if request.path.startswith(x)
            ]

            if len(flags) == 0:
                return redirect(url_for("setup.step1"))
        else:
            flags = [
                x for x in [
                    "/api",
                    "/static",
                    "/user/login",
                    "/setup/server-restart",
                ] if request.path.startswith(x)
            ]

            if len(flags) == 0:
                if "user" not in session.keys():
                    return redirect(url_for("user.login"))

        if "user" in session.keys() and isinstance(session['user'], dict):
            from app.models import User

            user = User.query.filter_by(
                id=session['user']['id']
            ).first()

            g.name = user.email.split("@")[0]
            g.email = user.email
            g.is_admin = user.is_admin

    return app
