
from flask import Blueprint


bp = Blueprint(
    name="dashboard",
    import_name="dashboard",
    url_prefix="/dashboard"
)


@bp.get("")
def index():
    return "TODO"
