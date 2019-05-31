
from __future__ import annotations

from typing import Mapping

import math

from facet.facet import Facet

from logcat.logcat import LogCat

class ExpPoint(Facet):
    DATA_PATH: str = 'null'
    _cache: Mapping[str, ExpPoint] = {}

    @LogCat.log_func
    def __init__(
        self
    ):
        self._exp = 0

    @LogCat.log_func
    def gain(self, exp: int) -> int:
        self._exp += exp

        return self._exp

    @property
    def value(self) -> int:
        return self._exp

# exp_point.py
