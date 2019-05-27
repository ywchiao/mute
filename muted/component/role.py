
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
        exp: int = 0,
        level: int = 1,
        name: str = '',
        room: str = ''
    ):
        self._exp = exp
        self._level = level
        self._name = name
        self._room = room

    @classmethod
    def _from_file(cls, entity: str, data: dict) -> str:
        cls._cache[entity] = cls(**data)

        return entity

    def enter(self, room: str) -> None:
        self._room = room

    @property
    def exp(self) -> str:
        return self._exp

    @property
    def level(self) -> str:
        return self._level

    @property
    def name(self) -> str:
        return self._name

    @property
    def room(self) -> str:
        return self._room

# role.py
