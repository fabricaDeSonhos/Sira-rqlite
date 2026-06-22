from flask import jsonify


def success_response(data=None, status_code=200):
    return jsonify({
        "success": True,
        "data": data,
    }), status_code


def error_response(message, code="ERROR", status_code=400):
    return jsonify({
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }), status_code