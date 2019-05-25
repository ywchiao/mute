
from const.color import Color
from widget.widget import Widget

from logcat.logcat import LogCat

class Button(Widget):
    @LogCat.log_func
    def __init__(self, x:int, y: int, text: str):
        super().__init__(x, y, 6)

        self._place_holder = ' ' * 6
        self._text = text

    @LogCat.log_func
    def paint(self, win):
        win.print_text(
            self.x, self.y,
            self._place_holder,
            Color.BUTTON
        )

        win.print_text(
            self.x + 1, self.y,
            self._text,
            Color.BUTTON
        )

# button.py
