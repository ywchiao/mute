
from typing import Mapping

from component.component import Component

class BoolComponent(Component):
    def __init__(self, data: Mapping[str, bool] = {}):
        self._cache = data

    def value(self, entity: str) -> bool:
        try:
            value = self._cache[entity]
        except KeyError:
            value = False

        return value

# bool_component.py
