
from flask import Blueprint


bp = Blueprint(
    name="download",
    import_name="download",
    url_prefix="/download"
)


@bp.get("/<string:file_id>")
@bp.get("/<string:file_id>/<string:fake>")
def file(file_id: str, fake=None):
    return f"download : {file_id} : {fake}"
