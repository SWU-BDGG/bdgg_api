from uuid import uuid4
from os.path import join
from hashlib import md5
from hashlib import sha256

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template

from app import UPLOAD_DIR
from app import db
from app.models import File
from app.check import check_login
from app.check import check_filename

from modules.encthread import Encryptor


bp = Blueprint(
    name="upload",
    import_name="upload",
    url_prefix="/upload"
)


@bp.get("")
def form():
    return render_template(
        "upload/form.html"
    )


@bp.post("")
def upload():
    user = check_login(bool_instead=True)

    if isinstance(user, bool):
        return abort(403)

    up_file = request.files.get("upload", None)

    if up_file is None:
        return redirect(url_for("upload.form", e="file_is_none"))

    file = File()
    file.uuid = uuid4().__str__()
    file.owner = user.id
    file.name = check_filename(up_file.filename)

    db.session.add(file)
    db.session.commit()

    up_file.save(join(UPLOAD_DIR, "__" + file.uuid))

    with open(join(UPLOAD_DIR, "__" + file.uuid), mode="rb") as r:
        stream = r.read()
        file.md5 = md5(stream).hexdigest()
        file.sha256 = sha256(stream).hexdigest()
        db.session.commit()

    Encryptor.queue_encryption(file.uuid, file.name, print)

    return redirect(url_for("upload.wait", file_id=file.uuid))


@bp.get("/wait/<string:file_id>")
def wait(file_id: str):
    return "wait for work"
