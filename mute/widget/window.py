
from __future__ import annotations

from const.color import Color
from event.event import Event
from viewport.viewport import Viewport
from widget.container import Container

from logcat.logcat import LogCat

class Window(Container):
    @LogCat.log_func
    def __init__(
        self, x: int, y:int, width: int, height: int, caption: str = None
    ):
        super().__init__(x, y, width, height)

        self._caption = caption
        self._focus = None

        self._win = Viewport(width, height)
        self._win.move_to(x, y)

        self._modal = False

        self.set_background(Color.TEXT)

        self.on(Event.CLICK, self._on_click)
        self.on(Event.KEY_PRESSED, self._on_key_pressed)
        self.on(Event.PAINT, self._on_paint)

    @LogCat.log_func
    def move(self, off_x: int, off_y: int) -> Window:
        self._win.move(off_x, off_y)

    @LogCat.log_func
    def set_background(self, color) -> Window:
        self._win.set_background(color)

        return self

    @LogCat.log_func
    def set_content(self, content) -> Window:
        self._content = content

        return self

    @LogCat.log_func
    def set_caption(self, caption: str) -> Window:
        self._caption = caption

        return self
    @LogCat.log_func
    def _on_any(self, e: Event) -> None:
        if self._focus:
            self._focus.on_event(e)

    @LogCat.log_func
    def _on_click(self, e: Event, x: int, y: int) -> bool:
        for widget in self.components:
            if widget.contains(x - self.x, y - self.y):
                Event.trigger(
                    Event(Event.CLICK, widget, x=x, y=y)
                )

                if widget.focusable:
                    self._focus = widget

                break

        return False

    @LogCat.log_func
    def _on_key_pressed(self, e: Event, key: str) -> None:
        if self._focus:
            self._focus.on_event(e)

    @LogCat.log_func
    def _on_paint(self, e: Event) -> None:
        (
            self._win
                .border()
                .print_text(1, 0, f'┨ {self._caption} ┠')
                .refresh()
        )

        for widget in self.components:
            widget.paint(self._win)

        if self._focus:
            self._focus.paint(self._win)

    @property
    def focused(self) -> bool:
        return self._focused

    @property
    def modal(self) -> bool:
        return self._modal

    @property
    def win(self) -> Viewport:
        return self._win

# window.py
