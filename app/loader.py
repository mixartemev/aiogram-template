from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.dispatcher.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.dispatcher.fsm.storage.redis import RedisStorage

from app import handlers, middlewares
from app.cfg import Cfg
from app.utils import logger
from app.utils.db import MyBeanieMongo

logger.setup_logger()

mongo = MyBeanieMongo()
storage = RedisStorage.from_url(Cfg.REDIS_DSN)

bt = Bot(token=Cfg.BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=storage)

admin_router = Router()
dp.include_router(admin_router)
regular_router = Router()
dp.include_router(regular_router)
handlers.setup_all_handlers(regular_router, admin_router)
middlewares.setup(dp)

ap = web.Application(debug=Cfg.APP_DEBUG)
setup_application(ap, dp, bot=bt)
SimpleRequestHandler(dispatcher=dp, bot=bt).register(ap, path=Cfg.BOT_PATH)
