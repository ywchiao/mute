
from __future__ import annotations

from const.color import Color
from widget.widget import Widget

from logcat.logcat import LogCat

class Label(Widget):
    @LogCat.log_func
    def __init__(self, x=0, y=0, text=''):
        super().__init__(x, y, len(text))

        self._text = text

    @LogCat.log_func
    def paint(self, win):
        win.print_text(
            self.x, self.y,
            self.text,
            Color.INPUT_FIELD
        )

    @property
    def text(self):
        return self._text

# label.py
