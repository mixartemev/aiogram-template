from aiogram import Dispatcher
from aiogram.types import BotCommand
from aiohttp import ClientSession


async def set_commands(dp: Dispatcher):  # Set command hints
    cmds = {
        'start': "Home page",
        # 'stocks_upd': "Update stocks from alor + T info",  # only for admins
        # 'withdraw': "Get your profit",
    }
    await dp.bot.set_my_commands(
        [BotCommand(cmd, description) for cmd, description in cmds.items()]
    )


async def post(url: str, json: dict = None, headers: dict = None):
    async with ClientSession() as session:
        async with session.post(url, json=json, headers=headers) as resp:
            return await resp.json()


async def get(url: str, params: dict = None, headers: dict = None):
    async with ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as resp:
            return await resp.json()
