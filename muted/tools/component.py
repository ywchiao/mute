
from __future__ import annotations

from typing import Optional
from typing import Sequence
from typing import Union

from pathlib import Path

import json

#from config.config import CONFIG
#from facet.facet import Facet

#from logcat.logcat import LogCat

class Component:
#    DATA_PATH = CONFIG.TEXT
    _cache = {}

    @classmethod
    def instance(cls, fname):
        if not fname in cls._cache:
            f = Path(f'./{fname}.json')

            if f.is_file():
                with f.open(encoding='utf-8') as fin:
                    try:
                        cls._cache[fname] = cls(json.load(fin))
                    except JSONDecodeError:
                        cls._cache[fname] = cls()

        return cls._cache[fname]

    def text(self, entity: str) -> str:
        return self._cache[entity]

    def value(self, entity: str) -> int:
        return self._cache[entity]

    def add(self, entity: str, value: Union[str, Sequence[str]]) -> None:
        self._cache[entity] = value

    def save(self) -> None:
        f = Path('./{self._fname}.json')

        print(json.dumps(self._cache, ensure_ascii=False, indent=2))

        with f.open(mode='w', encoding='utf-8') as fout:
            json.dump(self._cache, fout, ensure_ascii=False, indent=2)

# component.py
