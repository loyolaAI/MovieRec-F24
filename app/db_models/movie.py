from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from app.db_models import actor
from actor import Actor
from app.db_models import director
from director import Director

db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = "movies"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(nullable=True)
    revenue: Mapped[str] = mapped_column(nullable=True)
    release_data: Mapped[str] = mapped_column(nullable=True)
    poster_image_id: Mapped[str] = mapped_column(nullable=True)
    poster_image_url: Mapped[str] = mapped_column(nullable=True)

    actors: Mapped[list["Actor"]] = relationship("Actor", back_populates="movies")
    # List just incase a movie has more than one director
    directors: Mapped[list["Director"]] = relationship("Director", back_populates="movies")
