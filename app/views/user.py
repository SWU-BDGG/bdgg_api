
from flask import Blueprint


bp = Blueprint(
    name="user",
    import_name="user",
    url_prefix="/user"
)


@bp.get("/login")
def login():
    return "login.html"


@bp.post("/login")
def login_post():
    return "user.login_post"


@bp.get("/register")
def register():
    return "register.html"


@bp.post("/register")
def register_post():
    return "user.register_post"
