from sqlalchemy.orm import Mapped, mapped_column  # type: ignore

from app import db


class Movie(db.Model):
    __tablename__ = "movie_ratings"

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    # movie_title: Mapped[str] = mapped_column(nullable=False)
