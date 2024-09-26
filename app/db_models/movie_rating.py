from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy

from app.db_models import user
from user import User

db = SQLAlchemy()


class MovieRating(db.Model):
    __tablename__ = "movie_ratings"

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    id: Mapped[str] = mapped_column(db.ForeignKey("users.cuid"), nullable=False)
    movie_title: Mapped[str] = mapped_column(nullable=False)
    _rating: Mapped[float] = mapped_column(nullable=False)

    user: Mapped[User] = relationship(
        "User", back_populates="ratings"
    )  # Connects the relationshiop back to the User Model

    # Limits rating to 0 - 5
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not (0 <= value <= 5):
            raise ValueError("Rating must be between 0 and 5.")
        self._rating = value
