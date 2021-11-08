
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for

from app import db
from app.models import User
from app.models import Login
from app.check import check_login
from app.check import check_admin


bp = Blueprint(
    name="session",
    import_name="session",
    url_prefix="/session"
)


@bp.get("/remove/<int:session_id>")
def remove(session_id: int):
    login = Login.query.filter_by(
        id=session_id
    ).first()

    if login is not None:
        user = check_login(bool_instead=True)
        if isinstance(user, User):
            check_id = login.user_id == user.id
            if check_id or check_admin():
                db.session.delete(login)
                db.session.commit()

    back_to = request.referrer
    if back_to is None:
        back_to = url_for("user.dashboard.index")

    return redirect(back_to)


@bp.get("/remove/all")
def remove_all():
    user = check_login(bool_instead=True)

    if not isinstance(user, bool):
        Login.query.filter_by(
            user_id=user.id
        ).delete()
        db.session.commit()

    return redirect(url_for("user.logout"))
