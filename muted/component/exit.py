
from __future__ import annotations

from typing import Mapping
from typing import Optional

from config.config import CONFIG
from facet.facet import Facet

from logcat.logcat import LogCat

class Exit(Facet):
    DATA_PATH = CONFIG.EXIT
    _cache = {}

    @LogCat.log_func
    def __init__(
        self,
        **kwargs: Mapping[str, str]
    ):
        self._links = kwargs

    @LogCat.log_func
    def keys(self) -> str:
        return ', '.join(self._links.keys())

    @LogCat.log_func
    def to(self, d: str) -> Optional[str]:
        try:
            room = self._links[d]
        except KeyError:
            room = None

        return room

# exit.py
