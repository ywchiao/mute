
from __future__ import annotations

from typing import Mapping

from component.atr_str import AtrStr

from facet.facet import Facet

from logcat.logcat import LogCat

class AtkPower(Facet):
    DATA_PATH = 'null'
    _cache: Mapping[str, AtkPower] = {}

    @LogCat.log_func
    def __init__(
        self,
        entity: str = ''
    ):
        self._value = AtrStr.instance(entity).value

    @property
    def value(self) -> int:
        return self._value

# atk_power.py
