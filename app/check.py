from datetime import datetime

from flask import session

from app import db
from app.models import User
from app.models import Login


def clear_session() -> None:
    for key in list(session.keys()):
        del session[key]


def check_login() -> bool:
    session_user = session.get("user", {})
    user_id = session_user.get("id")
    token = session_user.get("token")

    if user_id is None or token is None:
        clear_session()
        return False

    user = User.query.filter_by(
        id=user_id
    ).first()

    if user is None:
        clear_session()
        return False

    login = Login.query.filter_by(
        user_id=user_id,
        token=token
    ).first()

    if login is None:
        clear_session()
        return False

    if login.expired < datetime.now():
        db.session.delete(login)
        db.session.commit()

        clear_session()
        return False

    return True


def check_admin():
    if not check_login():
        return False

    user = User.query.filter_by(
        id=session.get("user", {}).get("id", 0),
        is_admin=True
    ).first()

    if user is None:
        return False

    return True
