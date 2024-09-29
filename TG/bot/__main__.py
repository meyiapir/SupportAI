from __future__ import annotations

import asyncio

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from loguru import logger

from bot.core.config import settings
from bot.core.loader import bot, dp
from bot.handlers import get_handlers_router
from bot.keyboards.default_commands import set_default_commands
from bot.middlewares import register_middlewares


async def pinger() -> None:
    logger.debug("PING")


async def startup() -> None:
    register_middlewares(dp)
    dp.include_router(get_handlers_router())

    await set_default_commands(bot)

    bot_info = await bot.get_me()

    logger.info(f"Name     - {bot_info.full_name}")
    logger.info(f"Username - @{bot_info.username}")
    logger.info(f"ID       - {bot_info.id}")

    states: dict[bool | None, str] = {
        True: "Enabled",
        False: "Disabled",
        None: "Unknown (This's not a bot)",
    }

    logger.info(f"Groups Mode  - {states[bot_info.can_join_groups]}")
    logger.info(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logger.info(f"Inline Mode  - {states[bot_info.supports_inline_queries]}")

    logger.info("bot started")


async def shutdown() -> None:
    logger.info("bot stopping...")

    await dp.storage.close()
    await dp.fsm.storage.close()
    await bot.session.close()

    logger.info("bot stopped")


def main_webhook() -> None:
    logger.debug("bot starting...")
    logger.add(
        "logs/bot_debug.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="100 KB",
        compression="zip",
    )

    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=settings.WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=settings.HOST, port=settings.PORT)


async def main_polling() -> None:
    logger.debug("bot starting...")

    logger.add(
        "logs/bot_debug.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="100 KB",
        compression="zip",
    )

    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logger.debug(f"USE_WEBHOOK: {settings.USE_WEBHOOK}")
    if settings.USE_WEBHOOK:
        logger.info("USE WEBHOOK")
        main_webhook()
    else:
        logger.info("USE POLLING")
        asyncio.run(main_polling())
