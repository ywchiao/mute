
from __future__ import annotations

from config.config import CONFIG
from facet.facet import Facet

from logcat.logcat import LogCat

class Brief(Facet):
    DATA_PATH = CONFIG.BRIEF
    _cache = {}

    @LogCat.log_func
    def __init__(
        self,
        brief: str = f'沒說這個 [物件] 是什麼，就是個 [東西]。'
    ):
        self._brief = brief

    @property
    def text(self) -> str:
        return self._brief

# brief.py
