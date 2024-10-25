import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_migrate import Migrate  # type: ignore
from flask_login import LoginManager  # type: ignore
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass  # type: ignore

from app.exceptions import init_exception_handler

# Load environment variables from the .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Define a base class for SQLAlchemy models
class Base(DeclarativeBase, MappedAsDataclass):
    pass

# Initialize database and migration instances
db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app():
    """Application factory function to initialize the Flask app."""
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Load the database URL from environment variables
    pSQL_URL = os.getenv("POSTGRESQL_URL")
    if not pSQL_URL:
        raise ValueError("POSTGRESQL_URL environment variable is not set.")

    # Configure app settings
    app.config["SQLALCHEMY_DATABASE_URI"] = pSQL_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Set up login management
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """Load a user by their ID."""
        from app.db_models.user import User
        return User.query.get(str(user_id))

    # Register routes and exception handlers
    from .routes import init_routes
    init_routes(app)
    init_exception_handler(app)

    # Import database models to ensure they are registered
    from app.db_models.user import User
    from app.db_models.movie_rating import MovieRating
    from app.db_models.password_reset_token import PasswordResetToken

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
