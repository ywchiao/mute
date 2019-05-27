
from __future__ import annotations

from typing import List

from config.config import CONFIG
from facet.facet import Facet

from component.description import Description
from component.name import Name

from logcat.logcat import LogCat

class Room(Facet):
    DATA_PATH = CONFIG.ROOM
    _cache = {}

    @LogCat.log_func
    def __init__(
        self,
        name: str = '',
        brief: str = '',
        desc: str = '',
        npcs: list = []
    ):
        self._name = name
        self._brief = brief
        self._desc = desc
        self._guests = []
        self._npcs = npcs

    @LogCat.log_func
    def enter(self, entity: str) -> None:
        self._guests.append(entity)

    @LogCat.log_func
    def leave(self, entity: str) -> None:
        try:
            self._guests.remove(entity)
        except:
            pass

    @property
    def description(self) -> str:
        return Description.instance(self._desc).text

    @property
    def guests(self) -> List[str]:
        return self._guests

    @property
    def name(self) -> str:
        return Name.instance(self._name).text

# room.py
