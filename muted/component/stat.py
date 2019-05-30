
from __future__ import annotations

from typing import List

from config.config import CONFIG
from facet.facet import Facet

from component.brief import Brief
from component.description import Description

from logcat.logcat import LogCat

class Stat(Facet):
    DATA_PATH = CONFIG.Stat
    _cache = {}

    @LogCat.log_func
    def __init__(
        self,
        hp: int = 100,
        spr: int = 100
    ):
        self._hp = hp
        self._spr = desc

# stat.py
