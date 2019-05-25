
from __future__ import annotations

from const.color import Color
from event.event import Event
from widget.widget import Widget

from logcat.logcat import LogCat

class ScrollBar(Widget):
    ARROW_UP = '▲'
    ARROW_DOWN = '▼'
    ARROW_LEFT = '◄'
    ARROW_RIGHT = '►'
    INDICATOR = '◙'

    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)

        self._vertical = True
        self._place_holder = ' '
        self._at = y + 1

        if 1 == height:
            self._vertical = False
            self._place_holder = ' ' * width
            self._at = x + 1

        self.on(Event.CLICK, self._on_click)

    @LogCat.log_func
    def paint(self, win):
        if 1 == self.width:
            for y in range(1, self.height):
                win.print_text(
                    self.x, self.y + y,
                    self._place_holder, Color.SCROLL_BAR
                )

            win.print_text(
                self.left, self.bottom,
                ScrollBar.ARROW_DOWN, Color.TEXT
            )

            win.print_text(
                self.left, self.top,
                ScrollBar.ARROW_UP, Color.TEXT
            )

            win.print_text(
                self.left, self._at,
                ScrollBar.INDICATOR, Color.SCROLL_BAR
            )
        else:
            win.print_text(
                self.x, self.y,
                self._place_holder, Color.SCROLL_BAR
            )

            win.print_text(
                self.left, self.bottom,
                ScrollBar.ARROW_LEFT, Color.TEXT
            )

            win.print_text(
                self.right, self.bottom,
                ScrollBar.ARROW_RIGHT, Color.TEXT
            )

            win.print_text(
                self._at, self.bottom,
                ScrollBar.INDICATOR, Color.SCROLL_BAR
            )

    @LogCat.log_func
    def reset_to(self, r: float) -> None:
        self._at = int(r * (self.height - 2) + self.top + 1)

    @LogCat.log_func
    def _on_click(self, e: Event, x: int, y: int) -> None:
        if self._vertical:
            self._scroll_v(e, y)
        else:
            self._scroll_h(e, x)

    @LogCat.log_func
    def _scroll_h(self, e: Event, x: int) -> None:
        if x == self.left:
            Event.trigger(
                Event(Event.SCROLL_LEFT, e.target)
            )
        elif y == self.right:
            Event.trigger(
                Event(Event.SCROLL_RIGHT, e.target)
            )
        else:
            Event.trigger(
                Event(Event.SCROLL_H, e.target, r=(x - self.left)/self.width)
            )

    @LogCat.log_func
    def _scroll_v(self, e: Event, y: int) -> None:
        if y == self.top:
            Event.trigger(
                Event(Event.SCROLL_DOWN, e.target)
            )
        elif y == self.bottom:
            Event.trigger(
                Event(Event.SCROLL_UP, e.target)
            )
        else:
            r = (y - self.top - 1) / (self.height - 2)

            Event.trigger(
                Event(Event.SCROLL_V, e.target, r=r)
            )

# scroll_bar.py
