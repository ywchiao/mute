
from __future__ import annotations

import json

from pathlib import Path
from typing import Type

from logcat.logcat import LogCat

class Facet:
    @classmethod
    def instance(cls, entity: str, **kwargs) -> Type[Facet]:
        if not entity in cls._cache:
            path = Path(f'{cls.DATA_PATH}/{entity}.json')

            if path.is_file():
                with path.open(encoding='utf-8') as fin:
                    entity = cls._from_file(entity, json.load(fin))
            else:
                cls._cache[entity] = cls(**kwargs)

        return cls._cache[entity]

    @classmethod
    def _from_file(cls, entity: str, data: dict) -> str:
        for key, value in data.items():
            if dict == type(value):
                cls._cache[key] = cls(**value)
            else:
                cls._cache[key] = cls(value)

        return ""

# facet.py
