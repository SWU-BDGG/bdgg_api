
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import render_template

from app.check import check_login
from app.models import Login


bp = Blueprint(
    name="dashboard",
    import_name="dashboard",
    url_prefix="/dashboard"
)


@bp.get("")
def index():
    user = check_login(bool_instead=True)

    if isinstance(user, bool):
        return redirect(url_for("user.login"))

    login = Login.query.filter_by(
        user_id=user.id
    ).order_by(
        Login.date.desc()
    ).limit(15).all()

    return render_template(
        "user/dashboard.html",
        user=user,
        logins=login
    )


@bp.get("/file")
def file():
    return "TODO"
