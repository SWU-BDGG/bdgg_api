from hashlib import sha512

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app import db
from app.models import User
from app.config import update_config
from app.config.models import Database


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
    return render_template(
        "setup/step1.html"
    )


@bp.post("/step1")
def step1_post():
    database = Database(
        host=request.form.get("host", "#"),
        port=request.form.get("port", "#"),
        user=request.form.get("user", "#"),
        password=request.form.get("password", "#"),
        database=request.form.get("database", "#"),
    )

    update_config("Database", database)

    return redirect(url_for("setup.step2"))


@bp.get("/step2")
def step2():
    return render_template(
        "setup/step2.html"
    )


@bp.post("/step2")
def step2_post():
    email = request.form.get("email", None)
    password = request.form.get("password", None)

    if email is None or password is None:
        return redirect(url_for("setup.step2"))

    if len(password) < 8:
        return redirect(url_for("setup.step2"))

    user = User()
    user.email = email[:128]
    user.password = sha512(password.encode()).hexdigest()

    db.session.add(user)
    db.session.commit()

    return redirect("/")
