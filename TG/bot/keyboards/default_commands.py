from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from bot.utils.locales import translate

from bot.core.config import settings

commands = {}

for language in settings.LANGUAGES:
    commands.update({
        language: {
            "start": translate("start command", language),
            "language": translate("language command", language)
        }
    })


async def set_default_commands(bot: Bot) -> None:
    for language_code in commands:
        await bot.delete_my_commands(scope=BotCommandScopeDefault())

        await bot.set_my_commands(
            commands=[
                BotCommand(command=command, description=description)
                for command, description in commands[language_code].items()
            ],
            language_code=language_code
        )

        await bot.get_my_commands(scope=BotCommandScopeDefault(), language_code=language_code)
