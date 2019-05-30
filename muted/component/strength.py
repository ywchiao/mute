
from __future__ import annotations

from typing import Mapping

from facet.facet import Facet

from logcat.logcat import LogCat

class Strength(Facet):
    DATA_PATH: str = 'null'
    BASE: int = 10
    _cache: Mapping[str, Strength] = {}

    @LogCat.log_func
    def __init__(
        self,
        level: int = 1
    ):
        self._value = Strength.BASE + (level + 1) // 2

    @property
    def value(self) -> int:
        return self._value

# strength.py
