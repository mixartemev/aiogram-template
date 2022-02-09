from aiogram import Dispatcher

from app.handlers.private import default, start, help_, deposit


def setup(dp: Dispatcher):
    for module in (start, default, help_, deposit):
        module.setup(dp)
