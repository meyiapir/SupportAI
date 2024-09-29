from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column

from sender.database.models.base import Base, created_at, universal_id


class QuestionModel(Base):
    __tablename__ = "questions"

    id: Mapped[universal_id] = mapped_column(index=True)
    user_id: Mapped[str]
    question: Mapped[str]
    answer: Mapped[str]
    user_rate: Mapped[int | None]
    created_at: Mapped[created_at]
