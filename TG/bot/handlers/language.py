import os

from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.loader import bot
from bot.keyboards.inline.languages import languages_kb
from bot.services.users import set_language_code

router = Router(name="language")


@router.message(Command(commands=["language", "lang"]),)
async def language_handler(message: types.Message) -> None:
    await message.delete()
    await message.answer(_("language command"), reply_markup=languages_kb)

@router.callback_query(F.data.startswith("set_lang_"))
async def language_choice_handler(
        callback_query: types.CallbackQuery, session: AsyncSession
) -> None:
    language_code = callback_query.data.replace("set_lang_", "")
    await set_language_code(session, user_id=callback_query.from_user.id, language_code=language_code)

    await bot.send_message(callback_query.from_user.id, _("language selected"))
