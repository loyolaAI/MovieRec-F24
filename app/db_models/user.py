from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy

from app.db_models import movie_rating
from movie_rating import MovieRating

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    profile_image_id: Mapped[str] = mapped_column(nullable=True)
    profile_image_url: Mapped[str] = mapped_column(nullable=True)

    letterbox_username: Mapped[str] = mapped_column(unique=True)
    ratings: Mapped[list["MovieRating"]] = relationship(
        "MovieRating", back_populates="user"
    )  # Creates a relationship to MovieRating Model
