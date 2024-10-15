from flask import jsonify
from werkzeug.exceptions import HTTPException


def init_exception_handler(app):
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = jsonify(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.status_code = e.code
        return response
