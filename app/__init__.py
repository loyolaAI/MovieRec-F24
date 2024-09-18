from flask import Flask
from app.routes import init_routes
from app.exceptions import init_exception_handler


def create_app():
    app = Flask(__name__)
    init_routes(app)
    init_exception_handler(app)
    return app
