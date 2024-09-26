from flask import Flask
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

from app.routes import init_routes
from app.exceptions import init_exception_handler


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():  # Inits the db tables
        db.create_all()

    init_routes(app)
    init_exception_handler(app)
    return app
