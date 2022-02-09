from aiogram import Dispatcher
from aiogram.types import Message
from app.loader import _


async def get_start_message(m: Message):
    a = _("Hello, {name}!").format(
        name=m.from_user.full_name
    )
    await m.answer(a)


def setup(dp: Dispatcher):
    dp.message.register(get_start_message, commands="strt")
