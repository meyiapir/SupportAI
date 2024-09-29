from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.utils.i18n.core import I18n
from loguru import logger
from redis.asyncio import ConnectionPool, Redis

from bot.core.config import settings

token = settings.BOT_TOKEN

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

if settings.REDIS_URL:
    logger.debug("Using Redis from URL")
    redis_client = Redis.from_url(settings.REDIS_URL)
else:
    logger.debug("Using Redis from settings")
    redis_client = Redis(
        connection_pool=ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASS,
            db=0,
        ),
    )

storage = RedisStorage(
    redis=redis_client,
    key_builder=DefaultKeyBuilder(with_bot_id=True),
)

dp = Dispatcher(storage=storage)

i18n: I18n = I18n(path=settings.LOCALES_DIR, default_locale="en", domain=settings.I18N_DOMAIN)
