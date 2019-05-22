
from __future__ import annotations

from config.config import CONFIG
from facet.facet import Facet

from logcat.logcat import LogCat

class Role(Facet):
    DATA_PATH = CONFIG.ROLE
    _cache = {}

    @LogCat.log_func
    def __init__(
        self,
        name: str = '',
        room: str = ''
    ):
        self._name = name
        self._room = room

    @property
    def name(self) -> str:
        return self._name

    @property
    def room(self) -> str:
        return self._room

# role.py
