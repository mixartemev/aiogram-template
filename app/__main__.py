import logging

from aiohttp import web
from aiogram import Bot
from aiogram.dispatcher.fsm.state import StatesGroup, State

from app.cfg import Cfg
from app.loader import mongo, dp, ap, storage
from app.utils.set_bot_commands import set_commands
from app.utils.notifications.startup_notify import notify_superusers

from aiogram_dialog import Dialog, Window, DialogRegistry
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const


async def on_startup(bot: Bot):
    await bot.set_webhook(Cfg.WH_HOST+Cfg.BOT_PATH)
    await mongo.init_db()
    await notify_superusers(bot)
    await set_commands(bot)


async def on_shutdown(bot: Bot):
    logging.warning("Shutting down..")
    await storage.close()
    await mongo.close()
    await bot.delete_webhook()  # Remove webhook (not acceptable in some cases)
    await bot.session.close()
    logging.warning("Bye!")


# main dialog
class MainSG(StatesGroup):
    main = State()


main_menu = Dialog(
    Window(
        Const("Hello, unknown person"),
        Cancel(),
        state=MainSG.main
    )
)


if __name__ == '__main__':
    try:
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        registry = DialogRegistry(dp)
        registry.register_start_handler(MainSG.main)  # resets stack and start dialogs on /start command
        registry.register(main_menu)

        web.run_app(ap, port=Cfg.APP_PORT)

    except (KeyboardInterrupt, SystemExit):
        logging.info("Goodbye")
