from sqlalchemy.orm import Mapped, validates, mapped_column, relationship  # type: ignore
from sqlalchemy import ForeignKey  # type: ignore

from app import db


class MovieRating(db.Model):
    __tablename__ = "movie_ratings"

    id: Mapped[str] = mapped_column(primary_key=True)

    movie_id: Mapped[str] = mapped_column(ForeignKey("movies.movie_id"), nullable=False)
    movie: Mapped["Movie"] = relationship("Movie", back_populates="ratings")  # type: ignore

    _rating: Mapped[float] = mapped_column(nullable=False)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="ratings")  # type: ignore

    @validates("_rating")
    def validate_rating(self, key, value):
        if not (0 <= value <= 5):
            raise ValueError("Rating must be between 0 and 5.")
        return value
