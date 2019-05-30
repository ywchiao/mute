
from __future__ import annotations

import time

from logcat.logcat import LogCat

class Combat:
    @LogCat.log_func
    def __init__(self):
        super().__init__()

    @classmethod
    def instance(cls) -> Combat:
        if not cls._instance:
            cls._instance = Combat()

        return cls._instance

    @LogCat.log_func
    def enlist(self, attacker: str, defender: str) -> None:
        self._list.append((attacker, defender, time.time_ns()))
        self._list.append((attacker, offerder, time.time_ns()))

# combat.py
