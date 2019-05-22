
from __future__ import annotations

import uuid

from logcat.logcat import LogCat

class Entity:
    @classmethod
    def eid(self) -> str:
        return uuid.uuid4().hex

# entity.py
