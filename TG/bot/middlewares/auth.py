from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.config import settings
from bot.database.database import sessionmaker
from bot.services.users import add_user, user_exists


async def log_added_user(session, user, bot):
    await add_user(session=session, user=user)
    try:
        await bot.send_message(
            settings.LOG_GROUP_ID,
            f"👤 New user: <a href='tg://user?id={user.id}'>{user.full_name}</a>\nLink: tg://user?id={user.id}",
            disable_web_page_preview=False,
            message_thread_id=settings.NEW_USERS_TOPIC_ID,
        )
    except Exception as e:
        logger.error(str(e))


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)
        session: AsyncSession = data["session"]
        message: Message = event
        user = message.from_user
        bot = data["bot"]

        if not user:
            return await handler(event, data)

        if await user_exists(session, user.id):
            data["is_first_login"] = False

            return await handler(event, data)


        data["is_first_login"] = True

        logger.info(f"New User Registration | user_id: {user.id} | message: {message.text}")

        await log_added_user(session, user, bot)

        return await handler(event, data)
