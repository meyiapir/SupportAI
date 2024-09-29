from aiogram.fsm.state import State, StatesGroup


class UserMenu(StatesGroup):
    support = State()
    rating = State()
