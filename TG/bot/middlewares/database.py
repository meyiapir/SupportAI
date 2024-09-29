from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Update

from bot.database.database import sessionmaker


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: dict[str, Any],
    ) -> Any:
        async with sessionmaker() as session:
            data["session"] = session
            return await handler(event, data)
