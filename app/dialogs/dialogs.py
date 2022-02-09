from aiogram_dialog import Dialog

from .windows import start, deposit

start_dlg = Dialog(
    start.home_win,
)
deposit_dlg = Dialog(
    deposit.amount_select,
)