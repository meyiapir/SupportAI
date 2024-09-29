from aiogram import Router, types, F
from aiogram.utils.i18n import gettext as _
from loguru import logger
import traceback
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.questions import set_rate

router = Router(name="rate")


@router.callback_query(F.data.startswith('rate_'))
async def rate_handler(
    query: types.CallbackQuery,
    session: AsyncSession
) -> None:
    __, task_id, rate = query.data.split('_')

    await set_rate(session, question_id=task_id, rate=int(rate))

    await query.answer(_('rate set success').format(rate=rate))
