from aiogram import Router, types
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from bot.rabbitmq.publisher import publish
from bot.services.users import get_language_code

router = Router(name="support")


@router.message()
async def support_handler(
        message: types.Message,
        session: AsyncSession
) -> None:
    if message.text:
        question = message.text

        await message.answer(_('pending'))

    elif message.caption:
        question = message.caption

        await message.answer(_('media warning'))
        await message.answer(_('pending'))

    else:
        await message.answer(_('no text error'))
        await message.answer(_('start'))
        return

    language_code = await get_language_code(session, str(message.from_user.id))

    await publish(str(message.from_user.id), question, language_code)

