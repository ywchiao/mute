
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
        exits: dict = {},
        npcs: list = []
    ):
        self._name = name
        self._brief = brief
        self._desc = desc
        self._guests = []
        self._npcs = npcs
        self._exits = exits

    @LogCat.log_func
    def enter(self, entity: str) -> None:
        self._guests.append(entity)

    @LogCat.log_func
    def leave(self, entity: str) -> None:
        try:
            self._guests.remove(entity)
        except:
            pass

    @LogCat.log_func
    def multicast(self, msg):
        for guest in self._guests:
            guest.send(msg)

    @property
    def description(self) -> str:
        return Description.instance(self._desc).text

    @property
    def exits(self) -> str:
        if self._exits:
            return f'這裡明顯的出口有： {",".join(self._exits.keys())}'
        else:
            return f'這裡沒有出口。'

    @property
    def guests(self) -> List[str]:
        return self._guests

    @property
    def name(self) -> str:
        return Name.instance(self._name).text

# room.py
