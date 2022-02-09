from aiogram import Dispatcher
from aiogram.utils.i18n import SimpleI18nMiddleware

from .acl import ACLMiddleware
from .clocks import ClocksMiddleware
from .throttling import ThrottlingMiddleware
from app.loader import i18n


def setup(dp: Dispatcher):
    dp.message.middleware(ThrottlingMiddleware())
    # dp.callback_query.middlewares(ThrottlingMiddleware())
    dp.message.middleware(ClocksMiddleware())
    dp.callback_query.middleware(ClocksMiddleware())
    dp.update.outer_middleware(ACLMiddleware())
    dp.message.middleware(SimpleI18nMiddleware(i18n))
