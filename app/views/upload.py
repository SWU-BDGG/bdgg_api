
from flask import Blueprint
from flask import render_template


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
    return "upload.upload"
