
from __future__ import annotations

from typing import Mapping
from typing import Optional
from typing import Sequence

from config.config import CONFIG
from facet.facet import Facet

from logcat.logcat import LogCat

class Baggage(Facet):
    DATA_PATH: str = CONFIG.BAGGAGE
    _cache: Mapping[str, Baggage] = {}

    @LogCat.log_func
    def __init__(
        self,
        items: Sequence[str] = []
    ):
        self._items = items

    @property
    def items(self) -> Sequence[str]:
        return self._items

# baggage.py
