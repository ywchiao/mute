
from __future__ import annotations

import uuid

from event.event import Event
from event.handler import Handler

from logcat.logcat import LogCat

class Widget(Handler):
    @LogCat.log_func
    def __init__(self, x=0, y=0, width=1, height=1):
        super().__init__()

        self._uid = uuid.uuid4().hex
        self._focusable = True

        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @LogCat.log_func
    def contains(self, x: int, y: int) -> bool:
        if (
            x >= self.left and x <= self.right and
            y >= self.top and y <= self.bottom
        ):
           return True

        return False

    @property
    def bottom(self):
        return self._y + self._height - 1

    @property
    def focusable(self):
        return self._focusable

    @property
    def height(self):
        return self._height

    @property
    def left(self):
        return self._x

    @property
    def right(self):
        return self._x + self._width - 1

    @property
    def top(self):
        return self._y

    @property
    def uid(self):
        return self._uid

    @property
    def width(self):
        return self._width

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

# widget.py
