
from __future__ import annotations

from typing import Mapping

from config.config import CONFIG
from facet.facet import Facet

from logcat.logcat import LogCat

class Level(Facet):
    DATA_PATH: str = CONFIG.LEVEL
    _cache: Mapping[str, Level] = {}

    @LogCat.log_func
    def __init__(
        self,
        level: int = 1
    ):
        self._level = level

    @property
    def value(self) -> int:
        return self._level

# level.py
