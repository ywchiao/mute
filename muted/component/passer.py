
from __future__ import annotations

from typing import List

from config.config import CONFIG
from facet.facet import Facet

from component.genus import Genus
from component.name import Name
from component.npc import NPC

from logcat.logcat import LogCat

class Passer(Facet):
    DATA_PATH = CONFIG.PASSER
    _cache = {}

    @LogCat.log_func
    def __init__(
        self,
        passer: List[str] = []
    ):
        self._passer = passer

    @LogCat.log_func
    def enter(self, entity: str) -> None:
        self._passer.append(entity)

    @LogCat.log_func
    def leave(self, entity: str) -> None:
        try:
            self._passer.remove(entity)
        except ValueError:
            pass

    @LogCat.log_func
    def with_tag(self, tag: str) -> Optional[str]:
        for entity in self._passer:
            if tag == NPC.instance(entity).tag:
                break
        else:
            entity = None

        return entity

    @property
    def list(self) -> List[str]:
        return ', '.join([
            f'{Name.instance(Genus.instance(npc)).text} '
            f'({NPC.instance(Genus.instance(npc)).tag})'
            for npc in self._passer
        ])

# passer.py
