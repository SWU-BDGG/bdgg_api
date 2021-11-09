
from flask import Blueprint
from flask import Response
from flask import render_template

from app.models import File
from app.models import User
from app.custom_error import FileIsDeletedOrNotUploaded


bp = Blueprint(
    name="file",
    import_name="file",
    url_prefix="/"
)


@bp.get("")
def index():
    return "file.index"


@bp.get("/search")
def search():
    return "file.search"


@bp.get("/detail/<string:file_id>")
def detail(file_id: str):
    file = File.query.filter_by(
        uuid=file_id
    ).first()

    if file is None:
        raise FileIsDeletedOrNotUploaded

    upload_user = User.query.filter_by(
        id=file.owner
    ).first()

    return render_template(
        "file/detail.html",
        file=file,
        upload_user=upload_user
    )


@bp.get("/detail/<string:file_id>/checksum.txt")
def checksum(file_id: str):
    file = File.query.filter_by(
        uuid=file_id
    ).first()

    if file is None:
        raise FileIsDeletedOrNotUploaded

    return Response(
        mimetype="text/plain",
        response="\n".join([
            file.name,
            f"md5sum {file.md5}",
            f"sha256sum {file.sha256}",
        ])
    )
