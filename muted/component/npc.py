
from __future__ import annotations

from typing import List

from config.config import CONFIG
from facet.facet import Facet

from component.brief import Brief
from component.description import Description

from logcat.logcat import LogCat

class NPC(Facet):
    DATA_PATH = CONFIG.NPC
    _cache = {}

    @LogCat.log_func
    def __init__(
        self,
        brief: str = 'cd569caf9e024c63b961f4c2b4cc2e59',
        desc: str = 'b376927454d94fe4bf12cb2800188417',
        tag: str = 'lin-yan'
    ):
        self._brief = brief
        self._desc = desc
        self._tag = tag

    @property
    def brief(self) -> List[str]:
        return Brief.instance(self._brief).text

    @property
    def description(self) -> List[str]:
        return Description.instance(self._desc).text

    @property
    def tag(self) -> str:
        return self._tag

# npc.py
