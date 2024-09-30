from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_sqlalchemy import SQLAlchemy
from app.db_models import movie
from movie import Movie

db = SQLAlchemy()


class Director(db.Model):
    __tablename__ = "directors"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    movies: Mapped[list["Movie"]] = relationship("Movie", back_populates="actors")
