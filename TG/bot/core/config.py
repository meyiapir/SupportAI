from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class BotSettings(EnvBaseSettings):
    BOT_TOKEN: str
    RATE_LIMIT: int | float = 0.5

    WEBHOOK_HOST: str = "https://vds254.meyapir.ru"
    WEBHOOK_PATH: str = "/bot"
    WEBHOOK_URL: str = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WEBHOOK_SECRET: str = ""

    USE_WEBHOOK: bool = False


BOT_DIR = str(Path(__file__).absolute().parent.parent)
LOCALES_DIR = f"{BOT_DIR}/locales"
I18N_DOMAIN = "messages"
LANGUAGES = os.listdir(LOCALES_DIR)


class LocalesSettings(EnvBaseSettings):
    BOT_DIR: str = BOT_DIR
    LOCALES_DIR: str = LOCALES_DIR
    I18N_DOMAIN: str = I18N_DOMAIN
    LANGUAGES: list[str] = LANGUAGES


class DBSettings(EnvBaseSettings):
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str | None = None
    DB_NAME: str = "postgres"

    # PGPASSWORD: str = DB_PASS

    @property
    def database_url(self) -> URL | str:
        if self.DB_PASS:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql+asyncpg://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def database_url_psycopg2(self) -> str:
        if self.DB_PASS:
            return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql://{self.DB_USER}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class RedisSettings(EnvBaseSettings):
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASS: str | None = None
    REDIS_URL: str | None = None


class RabbitMQSettings(EnvBaseSettings):
    RMQ_ADDRESS: str = ""


class Settings(BotSettings, DBSettings, RabbitMQSettings, RedisSettings, LocalesSettings):
    pass


settings = Settings()
