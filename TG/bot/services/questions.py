from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from bot.database.models import QuestionModel


async def add_question(
        session: AsyncSession,
        user_id: str,
        question: str,
        answer: str,
) -> QuestionModel:
    """Add a new question to the database and return the created QuestionModel object."""
    new_question = QuestionModel(
        user_id=user_id,
        question=question,
        answer=answer,
        user_rate=None,  # Initial user rate set to 0 or default
    )

    session.add(new_question)
    await session.commit()
    await session.refresh(new_question)  # Refresh to get the updated object with any auto-generated fields like 'id'

    return new_question


async def set_rate(session: AsyncSession, question_id: str, rate: int) -> None:
    """Set the user rate for a question."""
    stmt = update(QuestionModel).where(QuestionModel.id == question_id).values(user_rate=rate)

    await session.execute(stmt)
    await session.commit()
