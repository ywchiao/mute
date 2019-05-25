
from __future__ import annotations

from const.color import Color
from event.event import Event
from widget.widget import Widget

from logcat.logcat import LogCat

class Field(Widget):
    @LogCat.log_func
    def __init__(self, x=0, y=0, width=80):
        super().__init__(x, y, width)

        self._text = ''
        self._place_holder = ' ' * width
        self._max_len = width

        self._color = Color.INPUT_FIELD

        self.on(
            Event.FOCUS_IN,
            lambda _: Event.trigger(Event(Event.CURSOR_ON))
        )
        self.on(
            Event.FOCUS_OUT,
            lambda _: Event.trigger(Event(Event.CURSOR_OFF))
        )
        self.on(Event.KEY_BACKSPACE, self._on_key_backspace)
        self.on(Event.KEY_PRESSED, self._on_key_pressed)

    @LogCat.log_func
    def paint(self, win):
        win.print_text(
            self.x, self.y,
            self._place_holder,
            self._color
        )

        win.print_text(
            self.x, self.y,
            self._text,
            self._color
        )

    @LogCat.log_func
    def _on_key_backspace(self, e: Event) -> None:
        self._text = self._text[:-1]

    @LogCat.log_func
    def _on_key_pressed(self, e: Event, key: str) -> None:
        if key in self._handlers:
            self._text = self._handlers[Event.LINEFEED](self._text)
        else:
            if key == Event.LINEFEED:
                key = ''

            self._text += key

    @property
    def value(self):
        return self._text

# field.py
