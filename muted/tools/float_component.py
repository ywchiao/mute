
from typing import Mapping

from component import Component

class FloatComponent(Component):
    def __init__(self, data: Mapping[str, float] = {}):
        self._cache = data

# float_component.py
