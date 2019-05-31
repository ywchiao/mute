
from __future__ import annotations

import time

from system.attack import Attack
from system.regen import Regen

from logcat.logcat import LogCat

class Timed:
    @staticmethod
    def update():
        t = time.time_ns()

        Attack.instance().update(t)
        Regen.instance().update(t)

# timed.py
