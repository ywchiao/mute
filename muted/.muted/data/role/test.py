
from __future__ import annotations

from typing import List

from pathlib import Path

import json

class Role:
    def __init__(
        self,
        name: str = '',
        room: str = ''
    ):
        self._name = name
        self._room = room

entity = 'moti'
path = Path(f'./{entity}.json')

_cache = {}

with path.open(encoding='utf-8') as fin:
    desc = json.load(fin)

    for key, value in desc.items():
        _cache[key] = Role(**value)
        print(_cache[key]._name)
        print(_cache[key]._room)

    print(_cache)
