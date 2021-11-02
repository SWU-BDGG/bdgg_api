from hashlib import sha512

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app import db
from app.models import User
from app.check import check_admin


bp = Blueprint(
    name="admin",
    import_name="admin",
    url_prefix="/admin"
)


@bp.get("")
def user_list():
    if not check_admin():
        return redirect(url_for("user.dashboard.index"))

    user = User.query.all()
    return render_template(
        "admin/list.html",
        user=user
    )


@bp.get("/edit/<int:user_id>")
def user_edit(user_id: int):
    if not check_admin():
        return redirect(url_for("user.dashboard.index"))

    user = User.query.filter_by(
        id=user_id
    ).first()

    if user is None:
        return redirect(url_for("admin.user_list"))

    return render_template(
        "admin/edit.html",
        user=user
    )


@bp.post("/edit/<int:user_id>")
def user_edit_post(user_id: int):
    if not check_admin():
        return redirect(url_for("user.dashboard.index"))

    user = User.query.filter_by(
        id=user_id
    ).first()

    if user is None:
        return redirect(url_for("admin.user_list"))

    user.email = request.form.get("email", user.email)

    if request.form.get("scope", "") == "admin":
        user.is_admin = True
    else:
        user.is_admin = False

    password = request.form.get("password")

    if len(password) >= 8:
        user.password = sha512(password.encode()).hexdigest()

    db.session.commit()

    return redirect(url_for("admin.user_list"))


@bp.get("/register")
def register():
    if not check_admin():
        return redirect(url_for("user.dashboard.index"))

    return render_template(
        "admin/register.html"
    )


@bp.post("/register")
def register_post():
    if not check_admin():
        return redirect(url_for("user.dashboard.index"))

    email = request.form.get("email")
    password = request.form.get("password")

    if len(email) == 0 or len(password) < 8:
        return redirect(url_for("admin.register"))

    user = User()
    user.email = email[:128]
    user.password = sha512(password.encode()).hexdigest()
    user.is_admin = False

    db.session.add(user)
    db.session.commit()

    return redirect(url_for("admin.user_list"))
