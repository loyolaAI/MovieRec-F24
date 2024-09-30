from werkzeug.security import generate_password_hash
from app.db_models.user import User
from app.db_models.password_reset_token import PasswordResetToken as Pass
from app import db

from typing import Callable
from datetime import datetime, timedelta
from cuid2 import cuid_wrapper  # type: ignore
import secrets

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
        reset_token=None,
    )


def get_user_by_email(email: str) -> User:
    return User.query.filter_by(email=email).first()


def create_reset_token(user: User) -> Pass:
    now = datetime.now()

    return Pass(
        id=cuid_generator(),
        email=user.email,
        token=f"{secrets.randbelow(1000000):06d}",  # 6 digit token, formatted as a string, and padded with 0s if necessary
        expires_at=now + timedelta(minutes=15),
        user_id=user.id,
        user=user,
    )


def delete_reset_token(token: Pass) -> None:
    db.session.delete(token)
    db.session.commit()


def get_reset_token(token: str) -> Pass:
    return Pass.query.filter_by(token=token).first()


def update_password(user: User, new_password: str) -> None:
    user.password = generate_password_hash(new_password)
    db.session.commit()
