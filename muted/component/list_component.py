
from __future__ import annotations

from typing import Mapping
from typing import Sequence

from component.component import Component

from logcat.logcat import LogCat

class ListComponent(Component):
    def __init__(self, fname: str):
        super().__init__(fname)

    @LogCat.log_func
    def append(self, entity: str, value: str) -> None:
        try:
            self._cache[entity].append(value)
        except KeyError:
            self._cache[entity] = [ value ]

    @LogCat.log_func
    def items(self, entity: str) -> Sequence[str]:
        try:
            items = *self._cache[entity],
        except KeyError:
            items = ()

        return items

    @LogCat.log_func
    def remove(self, entity: str, value: str) -> None:
        try:
            self._cache[entity].remove(value)
        except (KeyError, ValueError):
            pass

# list_component.py
