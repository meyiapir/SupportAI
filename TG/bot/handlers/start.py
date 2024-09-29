from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.i18n import gettext as _

router = Router(name="start")


@router.message(CommandStart())
async def support_handler(
        message: types.Message,
) -> None:
    await message.delete()
    await message.answer(_("start"))
