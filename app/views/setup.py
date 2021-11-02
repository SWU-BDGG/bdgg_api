from hashlib import sha512

from flask import Blueprint
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import current_app
from flask import render_template
from flask_migrate import upgrade
from sqlalchemy.exc import ProgrammingError

from app import db
from app.models import User
from app.config import update_config
from app.config.models import Database
from app.database import get_url


bp = Blueprint(
    name="setup",
    import_name="setup",
    url_prefix="/setup"
)


@bp.get("")
@bp.get("/")
def moveto():
    return redirect(url_for("setup.step1"))


@bp.get("/step1")
def step1():
    if get_url() != "#":
        return "데이터베이스 접속 정보가 이미 설정되어있습니다."

    return render_template(
        "setup/step1.html"
    )


@bp.post("/step1")
def step1_post():
    if get_url() != "#":
        return "데이터베이스 접속 정보가 이미 설정되어있습니다."

    database = Database(
        host=request.form.get("host", "#"),
        port=request.form.get("port", "#"),
        user=request.form.get("user", "#"),
        password=request.form.get("password", "#"),
        database=request.form.get("database", "#"),
    )

    update_config("Database", database)
    session['setup_step2'] = True
    session['user'] = "temp_login"

    return redirect(url_for("setup.step2"))


@bp.get("/step2")
def step2():
    if not session.get("setup_step2", False):
        return redirect(url_for("setup.step1"))

    if current_app.config['SQLALCHEMY_DATABASE_URI'] != get_url():
        return "데이터베이스 설정이 변경되어 서버 재시작이 필요합니다."

    return render_template(
        "setup/step2.html"
    )


@bp.post("/step2")
def step2_post():
    if not session.get("setup_step2", False):
        return redirect(url_for("setup.step1"))

    if current_app.config['SQLALCHEMY_DATABASE_URI'] != get_url():
        return "데이터베이스 설정이 변경되어 서버 재시작이 필요합니다."

    email = request.form.get("email", None)
    password = request.form.get("password", None)

    if email is None or password is None:
        return redirect(url_for("setup.step2"))

    if len(password) < 8:
        return redirect(url_for("setup.step2"))

    sv_restart_req = False

    try:
        if User.query.first() is not None:
            return "이미 관리자 유저가 생성되어있습니다."
    except ProgrammingError:
        upgrade()
        sv_restart_req = True

    user = User()
    user.email = email[:128]
    user.password = sha512(password.encode()).hexdigest()
    user.is_admin = True

    db.session.add(user)
    db.session.commit()

    del session['setup_step2']
    del session['user']

    if sv_restart_req:
        session['sv_restart_req'] = True
        return redirect(url_for(".plz_server_restart"))

    return redirect("/")


@bp.get("/server-restart")
def plz_server_restart():
    if session['sv_restart_req']:
        del session['sv_restart_req']
    else:
        return redirect("/")

    return "데이터베이스 설정이 변경되어 서버 재시작이 필요합니다."
