
from __future__ import annotations

from typing import Mapping

from facet.facet import Facet

from logcat.logcat import LogCat

class DefPower(Facet):
    DATA_PATH: str = 'null'
    _cache: Mapping[str, DefPower] = {}

    @LogCat.log_func
    def __init__(
        self,
        entity: str = ''
    ):
        self._value = 1

    @property
    def value(self) -> int:
        return self._value

# def_power.py
