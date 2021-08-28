
from flask import Blueprint


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
