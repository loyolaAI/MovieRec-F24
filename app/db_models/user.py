from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore

from app import db

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    profile_image_id: Mapped[str] = mapped_column(nullable=True)
    profile_image_url: Mapped[str] = mapped_column(nullable=True)

    letterbox_username: Mapped[str] = mapped_column(unique=True)
    ratings: Mapped[list["MovieRating"]] = relationship(back_populates="user") # type: ignore