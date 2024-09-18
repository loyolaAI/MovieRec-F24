from flask import Flask
from app.routes import init_routes

def create_app():
    app = Flask(__name__)
    init_routes(app)
    return app