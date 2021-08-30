
from flask import Blueprint
from flask import render_template


bp = Blueprint(
    name="setup",
    import_name="setup",
    url_prefix="/setup"
)


@bp.get("/step1")
def step1():
    return render_template(
        "setup/step1.html"
    )


@bp.get("/step2")
def step2():
    return render_template(
        "setup/step2.html"
    )
