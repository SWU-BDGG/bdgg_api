
from flask import jsonify


def on_error(message: str, code: str = "undefined", data: dict = None, api_version: str = "undefined"):
    return jsonify({
        "status": "error",
        "error": {
            "code": code,
            "message": message,
            "data": data if data is not None else {}
        },
        "api_version": api_version
    })


def on_success(data: dict, api_version: str = "undefined"):
    return jsonify({
        "status": "success",
        "data": data,
        "api_version": api_version
    })
