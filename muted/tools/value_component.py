
from typing import Mapping

from component import Component

class ValueComponent(Component):
    def __init__(self, data: Mapping[str, int] = {}):
        self._cache = data
        self._fname = 'value'

    def update(self, entity: str, value: int) -> None:
        self._cache[entity] = value

# value_component.py
