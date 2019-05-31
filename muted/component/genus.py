
from __future__ import annotations

import json

from pathlib import Path

from config.config import CONFIG

from logcat.logcat import LogCat

class Genus:
    DATA_PATH: str = CONFIG.GENUS
    _cache: Mapping[str, str] = None

    @classmethod
    def instance(cls, entity: str) -> str:
        if not cls._cache:
            path = Path(f'{cls.DATA_PATH}/{entity}.json')

            with path.open(encoding='utf-8') as fin:
                cls._cache = json.load(fin)
        else:
            try:
                entity = cls._cache[entity]
            except KeyError:
                pass

        return entity

# genus.py
