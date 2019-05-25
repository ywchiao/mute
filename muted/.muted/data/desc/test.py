
from __future__ import annotations

from typing import List

from pathlib import Path

import json

class Description():
    def __init__(
        self,
        desc: List[str] = [
            f'Muter 還沒有為這個 [物件] 建立任何描述；或者，更糟的',
            f'是，相關的內容已丟失或遺落在未知的時空。',
            f'如果可以，請你協助通知的相關人士，的未來掌握在看',
            f'到這段訊息的人手上。'
        ]
    ):
        self._desc = desc

    @property
    def text(self) -> List[str]:
        return self._desc

entity = 'default'
path = Path(f'./{entity}.json')

_cache = {}

with path.open(encoding='utf-8') as fin:
    desc = json.load(fin)

    for key, value in desc.items():
        _cache[key] = Description(value)
        print(_cache[key].text)

    print(_cache)
