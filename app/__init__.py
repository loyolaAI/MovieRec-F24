from flask import Flask # type: ignore
from sqlalchemy.orm import DeclarativeBase # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

from app.routes import init_routes
from app.exceptions import init_exception_handler


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    db.init_app(app)

    # from app.db_models.user import User
    # from app.db_models.movie_rating import MovieRating
    
    with app.app_context():
        db.create_all()

    init_routes(app)
    init_exception_handler(app)
    return app