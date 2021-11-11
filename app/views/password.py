from hashlib import sha512

from flask import Blueprint
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app import db
from app.models import User
from app.check import check_login


bp = Blueprint(
    name="password",
    import_name="password",
    url_prefix="/password"
)


class STEP:
    @staticmethod
    def get(step):
        return {
            1: url_for("user.password.step1"),
            2: url_for("user.password.step2"),
            3: url_for("user.password.step3"),
            None: url_for("user.password.step1"),
        }.get(step)


@bp.get("")
@bp.get("/")
def auto_redirect():
    password_change_step = session.get("password_change_step", None)
    return redirect(STEP.get(password_change_step))


@bp.get("/step1")
def step1():
    password_change_step = session.get("password_change_step", None)
    if isinstance(password_change_step, int):
        if password_change_step != 1:
            return redirect(STEP.get(password_change_step))

    return render_template(
        "password/step1.html"
    )


@bp.post("/step1")
def step1_post():
    password_change_step = session.get("password_change_step", None)
    if isinstance(password_change_step, int):
        if password_change_step != 1:
            return redirect(STEP.get(password_change_step))

    password = request.form.get("password", None)
    if password is None:
        return redirect(url_for("user.password.step1", e="pwn"))

    session_user = session.get("user", {})
    user_id = session_user.get("id")

    user = User.query.filter_by(
        id=user_id,
        password=sha512(password.encode()).hexdigest()
    ).first()

    if user is None:
        return redirect(url_for("user.password.step1", e="pwi"))

    session['password_change_step'] = 2
    return redirect(url_for("user.password.step2"))


@bp.get("/step2")
def step2():
    password_change_step = session.get("password_change_step", None)
    if isinstance(password_change_step, int):
        if password_change_step != 2:
            return redirect(STEP.get(password_change_step))

    return render_template(
        "password/step2.html"
    )


@bp.post("/step2")
def step2_post():
    password_change_step = session.get("password_change_step", None)
    if isinstance(password_change_step, int):
        if password_change_step != 2:
            return redirect(STEP.get(password_change_step))

    password = request.form.get("password", None)
    if password is None:
        return redirect(url_for("user.password.step2", e="pwn"))

    session['password_change_new'] = sha512(password.encode()).hexdigest()
    session['password_change_step'] = 3

    return redirect(url_for("user.password.step3"))


@bp.get("/step3")
def step3():
    password_change_step = session.get("password_change_step", None)
    if isinstance(password_change_step, int):
        if password_change_step != 3:
            return redirect(STEP.get(password_change_step))

    return render_template(
        "password/step3.html"
    )


@bp.post("/step3")
def step3_post():
    password_change_step = session.get("password_change_step", None)
    if isinstance(password_change_step, int):
        if password_change_step != 3:
            return redirect(STEP.get(password_change_step))

    password = request.form.get("password", None)
    if password is None:
        return redirect(url_for("user.password.step3", e="pwn"))

    if session['password_change_new'] == sha512(password.encode()).hexdigest():
        user = check_login(bool_instead=True)
        user.password = session['password_change_new']
        db.session.commit()
    else:
        return redirect(url_for("user.password.step3", e="pwi"))

    del session['password_change_new']
    del session['password_change_step']
    return redirect(url_for("user.dashboard.index"))
