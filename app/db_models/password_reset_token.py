import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore
from sqlalchemy import DateTime, ForeignKey  # type: ignore

from app import db


class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    token: Mapped[str] = mapped_column(nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", backref="", back_populates="reset_token")  # type: ignore
