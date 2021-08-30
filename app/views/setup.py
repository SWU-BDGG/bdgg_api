
from flask import Blueprint


bp = Blueprint(
    name="setup",
    import_name="setup",
    url_prefix="/setup"
)


@bp.get("/step1")
def step1():
    return "TODO"
