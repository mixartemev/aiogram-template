from aiogram.types import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Cancel, Button
from aiogram_dialog.widgets.text import Const

from app.dialogs.widgets.lang import Lang as _
from app.dialogs.sg import DepositSG
from app.dialogs.events.deposit import invoice, success_payment_handler

amount_select = Window(
    _('Input any amount or select one of the preset amount to deposit'),
    MessageInput(success_payment_handler, content_types=[ContentType.SUCCESSFUL_PAYMENT, ContentType.TEXT]),
    Group(
        Button(Const('1 000 ₽'), '1000', invoice),
        Button(Const('3 000 ₽'), '3000', invoice),
        Button(Const('10 000 ₽'), '10000', invoice),
        Button(Const('30 000 ₽'), '30000', invoice),
        Button(Const('100 000 ₽'), '100000', invoice),
        Cancel(_('Back', ' 🔙')),
        width=3
    ),
    state=DepositSG.amount,
    # preview_add_transitions=[Next()],  # sector_click to ticker_win
)
