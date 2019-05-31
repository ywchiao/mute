
from __future__ import annotations

from typing import Mapping

from facet.facet import Facet

from logcat.logcat import LogCat

class AtrStr(Facet):
    DATA_PATH: str = 'null'
    BASE: int = 10
    _cache: Mapping[str, AtrStr] = {}

    @LogCat.log_func
    def __init__(
        self,
        level: int = 1
    ):
        self._value = AtrStr.BASE + (level + 1) // 2

    @property
    def value(self) -> int:
        return self._value

# atr_str.py
