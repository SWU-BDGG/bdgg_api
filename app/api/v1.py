from hashlib import sha512
from secrets import token_bytes
from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import request
from flask import jsonify

from app import db
from app.models import User
from app.models import Login
from .resp import on_error
from .resp import on_success


bp = Blueprint(
    name="v1",
    import_name="v1",
    url_prefix="/v1"
)

API_VERSION = "v1"


@bp.post("/login")
def login():
    email = request.form.get("email", None)
    password = request.form.get("password", None)

    if email is None or password is None:
        return on_error(
            message="email of password is empty",
            code="api_login_fail_empty",
        ), 400

    pw_hashed = sha512(password.encode()).hexdigest()

    user = User.query.filter_by(
        email=email[:128],
        password=pw_hashed
    ).first()

    if user is None:
        return on_error(
            api_version=API_VERSION,
            message="fail to search user in database",
            code="api_login_fail_not_found"
        ), 404

    ls = Login()
    ls.user_id = user.id
    ls.user_agent = "[API] " + request.user_agent.string
    ls.token = token_bytes(64).hex()
    ls.expired = datetime.now() + timedelta(hours=6)

    db.session.add(ls)
    db.session.commit()

    return on_success(
        api_version=API_VERSION,
        data={
            "user": {
                "email": user.email
            },
            "session": {
                "token": ls.token,
                "expired": ls.expired.isoformat()
            }
        }
    )


@bp.get("/key")
def key():
    return jsonify({"status": "on dev"})


@bp.get("/download")
def download():
    auth = request.headers.get("authorization", default="undefined undefined")
    bearer, token = auth.split(" ")

    if bearer.lower() != "bearer":
        return on_error(
            message="",
        )

    return jsonify({"status": "on dev"})
