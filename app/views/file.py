from os.path import join

from flask import Blueprint
from flask import request
from flask import Response
from flask import redirect
from flask import url_for
from flask import render_template

from app import UPLOAD_DIR
from app import db
from app.models import File
from app.models import User
from app.models import Key
from app.custom_error import FileIsDeletedOrNotUploaded
from app.check import check_login


bp = Blueprint(
    name="file",
    import_name="file",
    url_prefix="/"
)


@bp.get("")
def index():
    try:
        page = int(request.args.get("page", "1"))

        if page <= 0:
            page = 1
    except ValueError:
        page = 1

    files = File.query.order_by(
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
        "file/list.html",
        files=files,
        pages=pages
    )


@bp.get("/search")
def search():
    filename = request.args.get("filename", None)

    if filename is not None and len(filename) >= 2:
        files = File.query.filter(
            File.name.ilike(f"%{filename}%")
        ).order_by(
            File.date.desc()
        ).limit(25).all()
    else:
        files = []

    return render_template(
        "file/search.html",
        files=files
    )


@bp.get("/detail/<string:file_id>")
def detail(file_id: str):
    user = check_login(bool_instead=True)

    if isinstance(user, dict):
        return redirect(url_for("user.login"))

    file = File.query.filter_by(
        uuid=file_id
    ).first()

    if file is None:
        raise FileIsDeletedOrNotUploaded

    upload_user = User.query.filter_by(
        id=file.owner
    ).first()

    key = Key.query.filter_by(
        uuid=file.uuid
    ).first()

    return render_template(
        "file/detail.html",
        file=file,
        upload_user=upload_user,
        key_status=True if key is not None else False,
        can_delete_able=user.id == upload_user.id or user.is_admin
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


@bp.get("/delete/<string:file_id>")
def delete(file_id: str):
    user = check_login(bool_instead=True)

    if isinstance(user, dict):
        return redirect(url_for("user.login"))

    file = File.query.filter_by(
        uuid=file_id
    ).first()

    if file is None:
        raise FileIsDeletedOrNotUploaded

    if file.owner == user.id or user.is_admin:
        Key.query.filter_by(
            uuid=file.uuid
        ).delete()

        db.session.delete(file)
        db.session.commit()

        getattr(__import__("os"), "remove")(join(UPLOAD_DIR, file.uuid))

        return redirect(url_for("file.index"))
    else:
        return redirect(url_for("file.detail", file_id=file_id))
