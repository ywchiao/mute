
from __future__ import annotations

from event.event import Event
from event.handler import Handler

from logcat.logcat import LogCat

class WindowManager(Handler):
    @LogCat.log_func
    def __init__(self):
        super().__init__()

        self._modal = None
        self._windows = {}
        self._z_stack = []

        self.on(Event.CLICK, self._on_click)
        self.on(Event.PAINT, self._on_paint)

    @LogCat.log_func
    def add(self, window: Window, modal: bool=False) -> None:
        self._windows[window.uid] = window

        if not modal:
            self._z_stack.append(window.uid)

    @LogCat.log_func
    def get_win(self, uid: str):
        return self._windows[uid]

    @LogCat.log_func
    def raise_to_top(self, uid):
        idx = self._z_stack.index(uid)
        self._z_stack.append(self._z_stack.pop(idx))

    @LogCat.log_func
    def hide_modal(self, uid: str) -> None:
        self._modal = None

    @LogCat.log_func
    def display(self, uid: str, display: bool) -> None:
        if display:
            self._modal = self._windows[uid]
        else:
            self._modal = None

    @LogCat.log_func
    def show_modal(self, uid: str) -> None:
        self._modal = self._windows[uid]

    @property
    def windows(self):
        return self._z_stack

    @LogCat.log_func
    def _on_click(self, e: Event, x: int, y: int) -> None:
        Event.trigger(
            Event(Event.FOCUS_OUT, self.focus)
        )

        if not self._modal:
            for uid in reversed(self._z_stack):
                if self._windows[uid].contains(x, y):
                    self.raise_to_top(uid)

                    break

        Event.trigger(
            Event(Event.CLICK, self.focus, x=x, y=y)
        )

        Event.trigger(
            Event(Event.FOCUS_IN, self.focus)
        )

    @LogCat.log_func
    def _on_paint(self, e: Event) -> None:
        for uid in self._z_stack:
            self._windows[uid].on_event(e)

        if self._modal:
            self._modal.on_event(e)

    @property
    def focus(self) -> Window:
        if self._modal:
            return self._modal
        else:
            return self._windows[self._z_stack[-1]]

# window_manager.py
