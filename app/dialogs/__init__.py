from aiogram_dialog.tools import render_transitions

from app.loader import registry
from .dialogs import start_dlg, deposit_dlg

registry.register(start_dlg)
registry.register(deposit_dlg)

render_transitions(registry)  # render graph with current transitions
