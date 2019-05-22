
from __future__ import annotations

import curses

from logcat.logcat import LogCat

class Viewport:
    @LogCat.log_func
    def __init__(self, width: int, height: int):
        self._win = curses.newwin(height, width, 0, 0)

        self._x = 0
        self._y = 0
        self._width = width
        self._height = height

    @LogCat.log_func
    def border(self) -> Viewport:
        self._win.box()

        return self

    @LogCat.log_func
    def move(self, off_x: int, off_y: int) -> None:
        self.move_to(self._y + off_y, self._x + off_x)

    @LogCat.log_func
    def move_cursor(self, x: int, y: int) -> None:
        self._win.move(y, x)
        y, x = self._win.getyx()
        LogCat.log(f'   move_cursor: x- {x} y- {y}')

    @LogCat.log_func
    def move_to(self, x: int, y: int) -> None:
        self._win.mvwin(y, x)

        self._y, self._x = self._win.getbegyx()

    @LogCat.log_func
    def print_line(
        self, x: int, y: int, text: str, attr: int = 0
    ) -> Viewport:
        self._win.addstr(y, x, f'{text}', attr)
        self._win.clrtoeol()
        self._win.refresh()

        return self

    @LogCat.log_func
    def print_text(
        self, x: int, y: int, text: str, attr: int = 0
    ) -> Viewport:
        self._win.addstr(y, x, f'{text}', attr)
        self._win.refresh()

        return self

    @LogCat.log_func
    def refresh(self) -> Viewport:
        self._win.refresh()

        return self

    @LogCat.log_func
    def set_background(self, color: int) -> Viewport:
        self._win.bkgd(' ', color)

        return self

    @property
    def bottom(self):
        return self._y + self._height - 1

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
    def width(self):
        return self._width

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

# viewport.py
