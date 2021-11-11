from os.path import join
from datetime import datetime

from flask import Blueprint
from flask import request
from flask import send_file

from app import UPLOAD_DIR
from app.models import Login
from app.models import File
from app.api.resp import on_error


bp = Blueprint(
    name="download",
    import_name="download",
    url_prefix="/download"
)

API_VERSION = "download"


@bp.get("/<string:file_id>")
def file(file_id: str):
    auth = request.headers.get("authorization", default="undefined undefined")
    bearer, token = auth.split(" ")

    if bearer.lower() != "bearer":
        return on_error(
            api_version=API_VERSION,
            message="this route requires `Bearer` token",
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

    file_from_db = File.query.filter_by(
        uuid=file_id
    ).first()

    if file_from_db is None:
        return on_error(
            api_version=API_VERSION,
            message="fail to find file in database",
            code="file_not_found"
        ), 404

    try:
        return send_file(
            join(UPLOAD_DIR, file_id),
            mimetype="application/octet-stream"
        )
    except FileNotFoundError:
        return on_error(
            api_version=API_VERSION,
            message="file is not encrypted",
            code="file_is_not_encrypted"
        ), 403
    except PermissionError:
        return on_error(
            api_version=API_VERSION,
            message="cannot access to file",
            code="call_manager_d1"
        ), 500
