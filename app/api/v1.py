
from flask import Blueprint
from flask import jsonify


bp = Blueprint(
    name="v1",
    import_name="v1",
    url_prefix="/v1"
)


@bp.post("/login")
def login():
    return jsonify({"status": "on dev"})


@bp.get("/key")
def key():
    return jsonify({"status": "on dev"})
