from flask import Flask  # type: ignore
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_login import LoginManager  # type: ignore

from app.exceptions import init_exception_handler
import os

from dotenv import load_dotenv

load_dotenv()


class Base(DeclarativeBase, MappedAsDataclass):
    pass


db = SQLAlchemy(model_class=Base)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "d2d2ad7660c18bdc8fc43e835c05a5f4928489eb0490aa00b862f2e1e7b74e15"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    from .routes import init_routes

    db.init_app(app)

    from app.db_models.user import User
    from app.db_models.movie_rating import MovieRating
    from app.db_models.password_reset_token import PasswordResetToken
    from app.db_models.movie import Movie

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(str(user_id))

    with app.app_context():
        # db.drop_all()
        db.create_all()

    init_routes(app)
    init_exception_handler(app)
    return app
