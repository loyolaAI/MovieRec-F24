from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore

from app import db


class Movie(db.Model):
    __tablename__ = "movies"  # Changed table name to 'movies'

    movie_id: Mapped[str] = mapped_column(primary_key=True)
    movie_title: Mapped[str] = mapped_column(nullable=False)
    movie_image: Mapped[str] = mapped_column(
        nullable=False, server_default="https://v0.dev/placeholder.svg"
    )

    # Back reference to MovieRating
    ratings: Mapped[list["MovieRating"]] = relationship("MovieRating", back_populates="movie")  # type: ignore

    def get_by_id(movie_id: str) -> "Movie":
        return Movie.query.filter_by(movie_id=movie_id).first()
