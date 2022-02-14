from app.loader import registry
from .dialogs import start_dlg, deposit_dlg

registry.register(start_dlg)
registry.register(deposit_dlg)
