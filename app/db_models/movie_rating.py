from sqlalchemy.orm import Mapped, validates, mapped_column, relationship  # type: ignore
from sqlalchemy import ForeignKey  # type: ignore

from app import db


class MovieRating(db.Model):
    __tablename__ = "movie_ratings"

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    movie_title: Mapped[str] = mapped_column(nullable=False)
    _rating: Mapped[float] = mapped_column(nullable=False)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", backref="", back_populates="ratings")  # type: ignore

    @validates("_rating")
    def validate_rating(self, key, value):
        if not (0 <= value <= 5):
            raise ValueError("Rating must be between 0 and 5.")
        return value
