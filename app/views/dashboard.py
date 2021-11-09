
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app.check import check_login
from app.models import File
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
    user = check_login(bool_instead=True)

    if isinstance(user, bool):
        return redirect(url_for("user.login"))

    try:
        page = int(request.args.get("page", "1"))

        if page <= 0:
            page = 1
    except ValueError:
        page = 1

    files = File.query.filter_by(
        owner=user.id
    ).order_by(
        File.date.desc()
    ).paginate(page)

    pages = []

    if files.page < 3:
        for i in range(1, files.pages + 1):
            if len(pages) == 5:
                break

            pages.append(i)
    else:
        for i in range(files.page - 2, files.pages + 1):
            if len(pages) == 5:
                break

            pages.append(i)

    return render_template(
        "user/file.html",
        files=files,
        pages=pages
    )
