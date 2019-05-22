
from __future__ import annotations

from config.config import CONFIG
from facet.facet import Facet

from logcat.logcat import LogCat

class Name(Facet):
    DATA_PATH = CONFIG.NAME
    _cache = {}

    @LogCat.log_func
    def __init__(
        self,
        name: str = '名字丟失'
    ):
        self._name = name

    @property
    def text(self) -> str:
        return self._name

# name.py
