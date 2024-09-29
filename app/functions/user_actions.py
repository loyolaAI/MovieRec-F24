from werkzeug.security import generate_password_hash
from app.db_models.user import User

from typing import Callable
from cuid2 import cuid_wrapper  # type: ignore

cuid_generator: Callable[[], str] = cuid_wrapper()


def create_user(email: str, username: str, password: str, letterboxd: str) -> User:
    return User(
        id=cuid_generator(),
        email=email,
        username=username,
        letterboxd_username=letterboxd,
        password=generate_password_hash(password),
        profile_image_id="",
        profile_image_url="",
        ratings=[],
    )


def get_user_by_email(email: str) -> User:
    return User.query.filter_by(email=email).first()
