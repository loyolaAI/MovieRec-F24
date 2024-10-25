from flask import Flask  # type: ignore
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_migrate import Migrate  # type: ignore
from flask_login import LoginManager  # type: ignore
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / '.env'  # Adjusting to point to the .env file
load_dotenv(dotenv_path=env_path)

from app.exceptions import init_exception_handler


class Base(DeclarativeBase, MappedAsDataclass):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    pSQL_URL = os.environ.get("POSTGRESQL_URL")
    if pSQL_URL is None:
        raise ValueError("POSTGRESQL_URL environment variable not set.")

    # app.config["SECRET_KEY"] = 
    app.config["SQLALCHEMY_DATABASE_URI"] = pSQL_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import init_routes

    from app.db_models.user import User
    from app.db_models.movie_rating import MovieRating
    from app.db_models.password_reset_token import PasswordResetToken

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
