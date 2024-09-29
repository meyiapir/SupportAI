from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from sender.database.models.base import Base, created_at, str_pk


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str_pk] = mapped_column(index=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    language_code: Mapped[str | None]
    created_at: Mapped[created_at]

    is_admin: Mapped[bool] = mapped_column(default=False)
    is_left: Mapped[datetime | None] = mapped_column(nullable=True)
