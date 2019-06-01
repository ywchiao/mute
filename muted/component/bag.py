
from __future__ import annotations

from typing import Mapping
from typing import Optional

from config.config import CONFIG
from facet.facet import Facet

from logcat.logcat import LogCat

class Bag(Facet):
    DATA_PATH: str = CONFIG.BAG
    _cache: Mapping[str, Bag] = {}

    @LogCat.log_func
    def __init__(
        self
    ):
        pass

# bag.py
