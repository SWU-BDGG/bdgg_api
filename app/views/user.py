from hashlib import sha512
from secrets import token_bytes
from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import abort
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import render_template

from app import db
from app.models import User
from app.models import Login
from . import dashboard


bp = Blueprint(
    name="user",
    import_name="user",
    url_prefix="/user"
)
bp.register_blueprint(dashboard.bp)


@bp.get("/logout")
def logout():
    for key in list(session.keys()):
        del session[key]

    return redirect(url_for("user.login"))


@bp.get("/login")
def login():
    if "user" in session.keys():
        return redirect(url_for("user.dashboard.index"))

    return render_template(
        "user/login.html"
    )


@bp.post("/login")
def login_post():
    email = request.form.get("email", None)
    password = request.form.get("password", None)

    if email is None or password is None:
        return abort(400)

    pw_hashed = sha512(password.encode()).hexdigest()

    user = User.query.filter_by(
        email=email[:128],
        password=pw_hashed
    ).first()

    if user is None:
        return redirect(url_for("user.login", err="user_not_found"))

    ls = Login()
    ls.user_id = user.idx
    ls.user_agent = request.user_agent
    ls.token = token_bytes(64).hex()
    ls.expired = datetime.now() + timedelta(hours=6)

    db.session.add(ls)
    db.session.commit()

    session['user'] = {
        "idx": user.idx,
        "token": ls.token
    }

    return redirect(url_for("user.dashboard.index"))
