from aiogram import Dispatcher

from app.handlers.private import default, help_, deposit


def setup(dp: Dispatcher):
    for module in (default, help_, deposit):
        module.setup(dp)
