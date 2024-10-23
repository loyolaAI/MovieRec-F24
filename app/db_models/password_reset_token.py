import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore
from sqlalchemy import DateTime, ForeignKey  # type: ignore

from app import db
from app.db_models.user import User

from typing import Callable
from cuid2 import cuid_wrapper  # type: ignore

cuid_generator: Callable[[], str] = cuid_wrapper()
import secrets


class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    token: Mapped[str] = mapped_column(nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", backref="", back_populates="reset_token")  # type: ignore

    def create_reset_token(user: User) -> "PasswordResetToken":
        from datetime import datetime, timedelta

        now = datetime.now()

        return PasswordResetToken(
            id=cuid_generator(),
            email=user.email,
            token=f"{secrets.randbelow(1000000):06d}",  # 6 digit token, formatted as a string, and padded with 0s if necessary
            expires_at=now + timedelta(minutes=15),
            user_id=user.id,
            user=user,
        )

    def delete_reset_token(token: "PasswordResetToken") -> None:
        token.user.reset_token = None
        db.session.delete(token)
        db.session.commit()

    def get_reset_token(token: str) -> "PasswordResetToken":
        return PasswordResetToken.query.filter_by(token=token).first()
