from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore
from flask_login import UserMixin
import werkzeug  # type: ignore
import os
from dotenv import load_dotenv

load_dotenv()

from app import db
from app.db_models.movie_rating import MovieRating

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    profile_image_id: Mapped[str] = mapped_column(nullable=False, server_default="")
    profile_image_url: Mapped[str] = mapped_column(nullable=False, server_default="")

    reset_token: Mapped["PasswordResetToken"] = relationship("PasswordResetToken", back_populates="user")  # type: ignore

    letterboxd_username: Mapped[str] = mapped_column(unique=True)
    ratings: Mapped[list["MovieRating"]] = relationship("MovieRating", back_populates="user", cascade="all, delete")  # type: ignore

    def get_id(self):
        return self.id

    def add_rating(self, rating: MovieRating) -> None:
        self.ratings.append(rating)

    def remove_rating(self, rating: MovieRating) -> None:
        self.ratings.remove(rating)
        db.session.delete(rating)
        db.session.commit()

    def get_by_email(email: str) -> "User":
        return User.query.filter_by(email=email).first()

    def get_by_letterboxd(letterboxd: str) -> "User":
        return User.query.filter_by(letterboxd_username=letterboxd).first()

    # to be implemented
    def upload_image(self, image: werkzeug.datastructures.file_storage.FileStorage) -> None:
        # Configuration
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            secure=True,
        )

        # Upload an image
        upload_result = cloudinary.uploader.upload(image)

        self.profile_image_url = upload_result["secure_url"]
        self.profile_image_id = upload_result["public_id"]
        db.session.commit()

    def delete_image(self) -> None:
        # Configuration
        cloudinary.config(
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            secure=True,
        )

        cloudinary.uploader.destroy(self.profile_image_id)
        self.profile_image_url = ""
        self.profile_image_id = ""
        db.session.commit()

    def has_rated_movie(self, movie_id: str) -> bool:
        for rating in self.ratings:
            if rating.movie_id == movie_id:
                return True
        return False

    def get_rating(self, movie_id: str) -> MovieRating:
        for rating in self.ratings:
            if rating.movie_id == movie_id:
                return rating
        return None

    def get_rated_movies(self) -> list["MovieRating"]:
        movies = []
        for rating in self.ratings:
            movies.append(rating.movie)
        return movies
