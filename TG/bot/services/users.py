from __future__ import annotations

from datetime import datetime  # noqa: TCH003

from aiogram.types import User  # noqa: TCH002
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: TCH002

from bot.cache.redis import build_key, cached, clear_cache
from bot.database.models import UserModel


async def add_user(
        session: AsyncSession,
        user: User,
        referrer: str | None = None,
) -> None:
    """Add a new user to the database."""
    user_id: int = user.id
    first_name: str = user.first_name
    last_name: str | None = user.last_name
    username: str | None = user.username
    language_code: str | None = user.language_code

    new_user = UserModel(
        id=str(user_id),
        first_name=first_name,
        last_name=last_name,
        username=username,
        language_code=language_code,
    )

    session.add(new_user)
    await session.commit()
    await clear_cache(user_exists, str(user_id))


async def delete_user(session: AsyncSession, user_id: int) -> None:
    """Delete user analytics from the database."""
    # Query for the specific user's analytics data
    await session.execute(
        delete(UserModel).where(UserModel.id == str(user_id))
    )
    await session.commit()
    # Clear cache after deletion
    await clear_cache(user_exists, str(user_id))


@cached(key_builder=lambda session, user_id: build_key(str(user_id)))
async def user_exists(session: AsyncSession, user_id: str) -> bool:
    """Checks if the user is in the database."""
    query = select(UserModel.id).filter_by(id=str(user_id)).limit(1)

    result = await session.execute(query)

    user = result.scalar_one_or_none()

    return bool(user)


@cached(key_builder=lambda session, user_id: build_key(str(user_id)))
async def get_first_name(session: AsyncSession, user_id: int) -> str:
    query = select(UserModel.first_name).filter_by(id=str(user_id))

    result = await session.execute(query)

    first_name = result.scalar_one_or_none()

    return first_name or ""


@cached(ttl=60, key_builder=lambda session, user_id: build_key(str(user_id)))
async def get_language_code(session: AsyncSession, user_id: str) -> str:
    query = select(UserModel.language_code).filter_by(id=str(user_id))

    result = await session.execute(query)

    language_code = result.scalar_one_or_none()

    return language_code or ""


async def set_language_code(
        session: AsyncSession,
        user_id: int,
        language_code: str,
) -> None:
    stmt = update(UserModel).where(UserModel.id == str(user_id)).values(language_code=language_code)
    await clear_cache(get_language_code, str(user_id))

    await session.execute(stmt)
    await session.commit()


@cached(key_builder=lambda session, user_id: build_key(str(user_id)))
async def is_admin(session: AsyncSession, user_id: int) -> bool:
    query = select(UserModel.is_admin).filter_by(id=str(user_id))

    result = await session.execute(query)

    is_admin = result.scalar_one_or_none()

    return bool(is_admin)


async def set_is_admin(session: AsyncSession, user_id: int, is_admin: bool) -> None:
    stmt = update(UserModel).where(UserModel.id == str(user_id)).values(is_admin=is_admin)

    await session.execute(stmt)
    await session.commit()


@cached(key_builder=lambda session: build_key())
async def get_all_users(session: AsyncSession) -> list[UserModel]:
    query = select(UserModel)

    result = await session.execute(query)

    users = result.scalars()

    return list(users)


@cached(key_builder=lambda session: build_key())
async def get_user_count(session: AsyncSession) -> int:
    query = select(func.count()).select_from(UserModel)

    result = await session.execute(query)

    count = result.scalar_one_or_none() or 0

    return int(count)


async def set_is_block(session: AsyncSession, user_id: int, block: bool) -> None:
    stmt = update(UserModel).where(UserModel.id == str(user_id)).values(is_block=block)

    await session.execute(stmt)
    await session.commit()


async def set_is_left(session: AsyncSession, user_id: int, left: datetime | None) -> None:
    stmt = update(UserModel).where(UserModel.id == str(user_id)).values(is_left=left)

    await session.execute(stmt)
    await session.commit()


async def is_left(session: AsyncSession, user_id: int) -> bool:
    query = select(UserModel.is_left).filter_by(id=str(user_id))
    result = await session.execute(query)

    result = result.fetchall()
    return result[0][0] is not None
