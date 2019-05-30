
from __future__ import annotations

from logcat.logcat import LogCat

class Regen:
    @LogCat.log_func
    def __init__(self):
        self._queue = []

    @LogCat.log_func
    def enlist(self, o):
        self._queue.append(o)

    def update(self, t_nano: int) -> None:
        self._queue = [
            (r, t + 5000000) for r, t in self._queue
                if (t_nano - t) > 5000000 and r.regen() < r.full_point
        ]

# regen.py
