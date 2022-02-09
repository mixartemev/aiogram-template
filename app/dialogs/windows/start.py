from aiogram.types import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Row, Cancel

from app.dialogs import sg
from app.dialogs.events.deposit import success_payment_handler_from_main
from app.dialogs.getters.start import get_home
from app.dialogs.widgets.lang import Lang as _

home_win = Window(
    _('Hi', '✌️ <b>{name}</b>!'),
    _('Your balance', '💲: <b>{bals}₽</b>'),
    Row(
        Start(_('Deposit', ' ₽🔼'), 'deposit', sg.DepositSG.amount),
        Cancel(),
    ),
    # MessageInput(success_payment_handler_from_main, content_types=ContentType.SUCCESSFUL_PAYMENT),
    state=sg.MainSG.home,
    getter=get_home
)
