
from __future__ import annotations

from typing import Mapping

import math

from facet.facet import Facet

from logcat.logcat import LogCat

class HitPoint(Facet):
    DATA_PATH: str = 'null'
    BASE: int = 31
    R: float = 1.047
    REGEN: int = 5
    _cache: Mapping[str, HitPoint] = {}

    @LogCat.log_func
    def __init__(
        self,
        level: int = 1
    ):
        self._hp = 10 * math.floor(
            HitPoint.BASE * math.pow(HitPoint.R, level - 1)
        )
        self._max = self._hp

    @LogCat.log_func
    def lose(self, point: int) -> int:
        self._hp = self._hp - point if self._hp > point else 0

        return self._hp

    @LogCat.log_func
    def regen(self) -> int:
        return self.restore(HitPoint.REGEN)

    @LogCat.log_func
    def restore(self, point: int) -> int:
        self._hp = self._hp + point

        if self._hp > self._max:
            self._hp = self._max

        return self._hp

    @property
    def max_value(self) -> int:
        return self._max

    @property
    def value(self) -> int:
        return self._hp

# hit_point.py
