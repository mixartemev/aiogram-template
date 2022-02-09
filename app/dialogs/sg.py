from aiogram.dispatcher.filters.state import StatesGroup, State


class MainSG(StatesGroup):
    home = State()


class DepositSG(StatesGroup):
    amount = State()

