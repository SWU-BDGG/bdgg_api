from re import compile
from datetime import datetime

from flask import session

from app.models import User
from app.models import Login


def check_filename(filename: str) -> str:
    # regex from `werkzeug.utils.secure_filename`
    pattern = compile(r"[^A-Za-z0-9가-힣_.-]")
    return str(pattern.sub("", "_".join(filename.split())).strip("._"))


def clear_session() -> None:
    for key in list(session.keys()):
        del session[key]


def check_login(bool_instead: bool = False) -> bool or User:
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
        clear_session()
        return False

    if bool_instead:
        return user

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
