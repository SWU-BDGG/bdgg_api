
from flask import session

from app.models import User
from app.models import Login


def check_login() -> bool:
    session_user = session.get("user", {})
    user_id = session_user.get("id")
    token = session_user.get("token")

    if user_id is None or token is None:
        return False

    user = User.query.filter_by(
        id=user_id
    ).first()

    if user is None:
        return False

    login = Login.query.filter_by(
        user_id=user_id,
        token=token
    )

    if login is None:
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
