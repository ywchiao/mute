
from __future__ import annotations

from typing import Any, Union

from event.event import Event

from logcat.logcat import LogCat

class Handler:
    @LogCat.log_func
    def __init__(self):
        self._handlers = {}

    @LogCat.log_func
    def on(self, key: Union[int, str], fun: function) -> None:
        self._handlers[key] = fun

    def on_event(self, e: Event) -> None:
        if e.type in self._handlers:
            self._handlers[e.type](e, **e.kwargs)
        else:
            self._on_any(e, **e.kwargs)

    @LogCat.log_func
    def _on_any(self, e: Event, **kwargs) -> None:
        pass

# handler.py
