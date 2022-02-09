from aiogram.types import PreCheckoutQuery
from aiogram import Dispatcher


async def process_pre_checkout_query(pcq: PreCheckoutQuery):  # invoice purchase is sent
    await pcq.answer(True)


def setup(dp: Dispatcher):
    dp.pre_checkout_query.register(process_pre_checkout_query)
