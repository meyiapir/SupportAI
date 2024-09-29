from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def rate_keyboard(task_id) -> InlineKeyboardMarkup:
    rate_range = (1, 2, 3, 4, 5)

    buttons = [[]]

    for rate in rate_range:
        buttons[0].append(
            InlineKeyboardButton(text=str(rate), callback_data=f'rate_{task_id}_{rate}')
        )

    keyboard = InlineKeyboardBuilder(markup=buttons)

    return keyboard.as_markup()
