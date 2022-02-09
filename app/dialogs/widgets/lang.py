from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.text.format import _FormatDataStub
from aiogram_dialog.widgets.when import WhenCondition
from app.loader import _


class Lang(Text):
    def __init__(self, trans: str, form: str = '', qty: str = None, plural: str = None, when: WhenCondition = None):
        super().__init__(when)
        self.text = trans
        self.sfx = form
        self.plural = plural
        self.qty = qty

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        if manager.is_preview():
            data = _FormatDataStub(data=data)
        qty = data[self.qty] if self.qty else 1
        trans = _(self.text, self.plural, qty)
        form = trans.format_map(data)
        res = form + self.sfx.format_map(data)
        return res
