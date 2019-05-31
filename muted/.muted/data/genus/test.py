
from __future__ import annotations

import json

from pathlib import Path

_cache: Mapping[str, str] = None

if not _cache:
    path = Path(f'./default.json')

    with path.open(encoding='utf-8') as fin:
        _cache = json.load(fin)

print(type(_cache))
print(json.dumps(_cache))

