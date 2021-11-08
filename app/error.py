
from flask import render_template

from .custom_error import *


class BDGGError:
    def __init__(self, code: int or str):
        self.file_name = f"error/{code}.html"

    def html(self, e):
        return render_template(
            self.file_name,
            e=e
        )


error_map = {
    # HTTP Error
    400: BDGGError(400),
    403: BDGGError(403),
    404: BDGGError(404),

    # Custom Error
    FileIsDeletedOrNotUploaded: BDGGError("file_is_deleted_or_not_uploaded"),
}


