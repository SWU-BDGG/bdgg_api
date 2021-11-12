from hashlib import sha512
from secrets import token_bytes
from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import request

from app import db
from app.models import File
from app.models import User
from app.models import Login
from app.models import Key
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
            api_version=API_VERSION,
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
    ), 201


@bp.get("/key")
def key():
    auth = request.headers.get("authorization", default="undefined undefined")
    bearer, token = auth.split(" ")

    if bearer.lower() != "bearer":
        return on_error(
            api_version=API_VERSION,
            message="this api requires `Bearer` token",
            data={
                "ex": "Authorization: Bearer {YOUR_TOKEN}"
            },
            code="required_authorization"
        ), 403

    session = Login.query.filter_by(
        token=token
    ).first()

    if session is None or session.expired < datetime.now():
        return on_error(
            api_version=API_VERSION,
            message="Expired authorization token",
            code="expired_token"
        ), 403

    file_id = request.args.get("file_id", None)

    if file_id is None:
        return on_error(
            api_version=API_VERSION,
            message="this api requires `file_id`",
            data={
                "ex": "/api/{API_VERSION}/key?file_id={YOUR_FILE_ID}"
            },
            code="file_id_missing"
        ), 400

    file_from_db = File.query.filter_by(
        uuid=file_id
    ).first()

    if file_from_db is None:
        return on_error(
            api_version=API_VERSION,
            message="fail to find file in database",
            code="file_not_found"
        ), 404

    key_from_db = Key.query.filter_by(
        uuid=file_from_db.uuid
    ).first()

    if key_from_db is None:
        return on_error(
            api_version=API_VERSION,
            message="file is not encrypted yet",
            code="file_decrypt_key_not_found"
        ), 400

    return on_success(
        api_version=API_VERSION,
        data={
            "file_id": file_from_db.uuid,
            "file": {
                "filename": file_from_db.name,
                "md5": file_from_db.md5,
                "sha256": file_from_db.sha256,
            },
            "key": {
                "key": key_from_db.key,
                "iv": key_from_db.iv
            }
        }
    )
