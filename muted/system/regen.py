
from __future__ import annotations

from typing import List

import time

from logcat.logcat import LogCat

class Regen:
    _instance: Regen = None

    @LogCat.log_func
    def __init__(self):
        self._queue = []

    @classmethod
    def instance(cls) -> Regen:
        if not cls._instance:
            cls._instance = Regen()

        return cls._instance

    @LogCat.log_func
    def enlist(self, o):
        self._queue.append((o, time.time_ns()))

    def update(self, t_ns: int) -> None:
        queue = []

        for r, t in self._queue:
            if t_ns - t > 5000000000:
                r.regen()

                if r.value < r.max_value:
                    queue.append((r, t + 5000000000))
            else:
                queue.append((r, t))

        self._queue = queue

# regen.py
