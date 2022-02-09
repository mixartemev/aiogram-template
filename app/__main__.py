import logging

from aiohttp import web
from aiogram import Bot

from app import middlewares, handlers
from app.cfg import Cfg
from app.loader import mongo, dp, ap, storage, registry, regular_router, admin_router
from app.utils.set_bot_commands import set_commands
from app.utils.notifications.startup_notify import notify_superusers
from app.dialogs.sg import MainSG

from aiogram_dialog.tools import render_transitions, render_preview


async def on_startup(bot: Bot):
    await bot.set_webhook(Cfg.WH_HOST+Cfg.BOT_PATH)
    await mongo.init_db()
    await notify_superusers(bot)
    await set_commands(bot)
    await render_preview(registry, "preview.html")  # render windows preview
    render_transitions(registry)  # render graph with current transtions


async def on_shutdown(bot: Bot):
    logging.warning("Shutting down..")
    await storage.close()
    await mongo.close()
    await bot.delete_webhook()  # Remove webhook (not acceptable in some cases)
    await bot.session.close()
    logging.warning("Bye!")


if __name__ == '__main__':
    try:
        middlewares.setup(dp)
        handlers.setup_all_handlers(regular_router, admin_router)

        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        registry.register_start_handler(MainSG.home)  # resets stack and start dialogs on /start command

        web.run_app(ap, port=Cfg.APP_PORT)

    except (KeyboardInterrupt, SystemExit):
        logging.info("Goodbye")
