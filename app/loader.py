from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.dispatcher.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.dispatcher.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.utils.i18n.core import I18n

from aiogram_dialog import DialogRegistry

from app.cfg import Cfg
from app.utils import logger
from app.utils.db import MyBeanieMongo

logger.setup_logger()

mongo = MyBeanieMongo()
storage = RedisStorage.from_url(Cfg.REDIS_DSN, key_builder=DefaultKeyBuilder(with_destiny=True))

bt = Bot(token=Cfg.BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=storage)

registry = DialogRegistry(dp)  # for dialogs

admin_router = Router()
dp.include_router(admin_router)
regular_router = Router()
dp.include_router(regular_router)

ap = web.Application(debug=Cfg.APP_DEBUG)
setup_application(ap, dp, bot=bt)
SimpleRequestHandler(dispatcher=dp, bot=bt).register(ap, path=Cfg.BOT_PATH)

i18n = I18n(path='locales', default_locale="en", domain='dd')
_ = i18n.gettext
