import decimal
from typing import List

from aiogram import types, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram_dialog import DialogManager, Dialog
from aiogram_dialog.widgets.kbd import Button

from app.cfg import Cfg
from app.helpers.money import m_form
from app.loader import _


async def invoice(c: CallbackQuery, btn: Button, mng: DialogManager):
    amount = int(btn.widget_id)
    await _send_invoice(amount, mng)


async def _send_invoice(amount, mng: DialogManager):
    uid = mng.event.from_user.id
    s = 'custom' if hasattr(mng.event, 'text') else 'button'
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=_('Deposit')+' ₽', pay=True),
        InlineKeyboardButton(text=_('Cancel')+' 🔙', callback_data='cancel:' + s)
    ]])
    bot: Bot = mng.data['bot']
    await bot.send_invoice(uid,
                           title=_('Balance charging') + f' {m_form(amount)} ₽',
                           description=_('For using service'),
                           provider_token=Cfg.PAY_TOKEN,
                           currency='rub',
                           is_flexible=False,  # True если конечная цена зависит от способа доставки
                           prices=_prices_with_fee(amount, fee=2.3),
                           start_parameter='balance-charge',
                           payload=amount,
                           reply_markup=kb
                           )


def _prices_with_fee(amount: int, fee: decimal = 2.3) -> List[types.LabeledPrice]:  # prices gen helper
    return [
        types.LabeledPrice(
            label=_('Resulting charge amount'),
            amount=amount * 100
        ),
        types.LabeledPrice(
            label=_('Acquiring fee') + f' {fee}%',
            amount=int(amount * fee)
        )
    ]


async def success_payment_handler(msg: Message, dlg: Dialog, mng: DialogManager):  # payment received or custom amount
    if msg.successful_payment:
        await _tsact_save(msg, mng)
        await mng.done()
    else:
        if str(amount := int(msg.text)) != msg.text:
            return await msg.answer(_('Input only DIGITS of ₽ amount please!'))
        elif (amount := int(amount)) < 10:
            return await msg.answer(_('You can not deposit less than 10₽'))
        # await msg.bot.delete_message(msg.chat.id, msg.message_id)
        await _send_invoice(amount, mng)
        await mng.mark_closed()


async def success_payment_handler_from_main(msg: Message, dlg: Dialog, mng: DialogManager):
    await _tsact_save(msg, mng)


async def _tsact_save(msg: Message, mng: DialogManager):
    suc_pay = msg.successful_payment
    amount = int(suc_pay.invoice_payload)
    # prf: Profile = (await mng.data['state'].get_data())['prf']
    # await prf.load(db, 0)
