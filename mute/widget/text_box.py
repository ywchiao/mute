
from __future__ import annotations

from const.color import Color
from event.event import Event
from widget.scroll_bar import ScrollBar
from widget.widget import Widget

from logcat.logcat import LogCat

class TextBox(Widget):
    @LogCat.log_func
    def __init__(self, x=0, y=0, width=1, height=1):
        super().__init__(x, y, width, height)

        self._text = []
        self._top_line = 0
        self._place_holder = ' ' * width
#        self._hbar = ScrollBar(1, y + height - 1, width, 1)
        self._vbar = ScrollBar(x + width - 1, 1, 1, height - 1)

        self.on(Event.CLICK, self._on_click)
        self.on(Event.KEY_UP, self._on_scroll_down)
        self.on(Event.KEY_DOWN, self._on_scroll_up)
        self.on(Event.SCROLL_DOWN, self._on_scroll_down)
        self.on(Event.SCROLL_UP, self._on_scroll_up)
        self.on(Event.SCROLL_V, self._on_scroll_v)

    @LogCat.log_func
    def add_text(self, text):
        self._text.append(text)

        if len(self._text) >= self.height:
            self._top_line += 1
            self._adjust_scroll_bar()

    @LogCat.log_func
    def paint(self, win):
        for y in range(1, self._height):
            line = self._top_line + y - 1

            if line >= len(self._text):
                break

            win.print_text(
                1, y,
                self._place_holder,
                Color.TEXT
            )

            win.print_text(
                1, y,
                self._text[line],
                Color.TEXT
            )

#        self._hbar.paint(win)
        self._vbar.paint(win)

    @LogCat.log_func
    def _adjust_scroll_bar(self) -> None:
        r = self._top_line / (len(self._text) - self.height + 1)
        self._vbar.reset_to(r)

    @LogCat.log_func
    def _on_click(self, e: Event, x: int, y: int) -> None:
        if self._vbar.contains(x, y):
            self._vbar.on_event(e)

    @LogCat.log_func
    def _on_scroll_down(self, e: Event) -> None:
        self._top_line -= 1 if self._top_line else 0

        self._adjust_scroll_bar()

    @LogCat.log_func
    def _on_scroll_up(self, e: Event) -> None:
        if (self._top_line + self.height) < len(self._text):
            self._top_line += 1

            self._adjust_scroll_bar()

    @LogCat.log_func
    def _on_scroll_v(self, e: Event, r: float) -> None:
        if len(self._text) > (self.height - 1):
            self._top_line = int((len(self._text) - self.height + 1) * r)
        else:
            self._top_line = 0
            r = 0

        self._vbar.reset_to(r)

# text_box.py
