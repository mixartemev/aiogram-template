from aiogram.dispatcher.fsm.context import FSMContext
from aiogram_dialog import DialogManager


async def get_home(dialog_manager: DialogManager, state: FSMContext, **kwargs):
    user = dialog_manager.event.from_user
    return {
        'name': user.full_name,
        'bals': 0,
    }
