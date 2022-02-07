import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.dispatcher.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app import handlers, middlewares
from app.config import Config
from app.utils import logger
from app.utils.db import MyBeanieMongo
from app.utils.db.mongo_storage import MongoStorage
from app.utils.notifications.startup_notify import notify_superusers
from app.utils.set_bot_commands import set_commands

WEB_SERVER_PORT = 8081
BOT_PATH = f"/wh/{Config.BOT_TOKEN}"

mongo = MyBeanieMongo()
storage = MongoStorage.from_url(
    Config.MONGODB_URI,
    f"{Config.MONGODB_DATABASE}_fsm",
)


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.set_webhook(Config.WH_HOST+BOT_PATH)
    await mongo.init_db()
    await notify_superusers(bot)
    await set_commands(bot)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.warning("Shutting down..")
    await bot.session.close()
    storage.close()
    await mongo.close()
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()
    logging.warning("Bye!")


def main():
    bot = Bot(token=Config.BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    admin_router = Router()
    dp.include_router(admin_router)
    regular_router = Router()
    dp.include_router(regular_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    middlewares.setup(dp)
    handlers.setup_all_handlers(regular_router, admin_router)
    logger.setup_logger()

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=BOT_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, port=WEB_SERVER_PORT)
