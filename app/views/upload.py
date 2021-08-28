
from flask import Blueprint


bp = Blueprint(
    name="upload",
    import_name="upload",
    url_prefix="/upload"
)


@bp.get("")
def form():
    return "form.html"


@bp.post("")
def upload():
    return "upload.upload"
