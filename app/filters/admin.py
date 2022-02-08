from aiogram import types
from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import TelegramObject

from app.cfg import Cfg


class AdminFilter(BaseFilter):

    async def __call__(self, obj: TelegramObject, event_from_user: types.User) -> bool:
        return str(event_from_user.id) in Cfg.ADMINS
