
from flask import Blueprint

from app import api


bp = Blueprint(
    name="api",
    import_name="api",
    url_prefix="/api"
)


for version in api.__all__:
    bp.register_blueprint(blueprint=getattr(getattr(api, version), "bp"))
