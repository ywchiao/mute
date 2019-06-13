
from __future__ import annotations

from typing import Any
from typing import Mapping
from typing import Type

from pathlib import Path

import json

from config.config import CONFIG

from logcat.logcat import LogCat

class Component:
    DATA_PATH = CONFIG.DATA_ROOT
    _cache: Mapping[str, Type[Component]] = {}

    def __init__(self, fname: str):
        f = Path(f'{Component.DATA_PATH}/{fname}.json')

        if f.is_file():
            with f.open(encoding='utf-8') as fin:
                try:
                    self._cache = json.load(fin)
                except json.decoder.JSONDecodeError:
                    self._cache = {}
        else:
            self._cache = {}

    @classmethod
    def instance(cls, fname: str) -> Type[Component]:
        if not fname in cls._cache:
            cls._cache[fname] = cls(fname)

        return cls._cache[fname]

    def save(self, fname: str) -> None:
        f = Path(f'./tools/data/{fname}.json')

        print(json.dumps(self._cache, ensure_ascii=False, indent=2))

        with f.open(mode='w', encoding='utf-8') as fout:
            json.dump(self._cache, fout, ensure_ascii=False, indent=2)

    def update(self, entity: str, value: Any) -> None:
        self._cache[entity] = value

# component.py
