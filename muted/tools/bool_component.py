
from typing import Mapping

from component import Component

class BoolComponent(Component):
    def __init__(self, data: Mapping[str, bool] = {}):
        self._cache = data

# bool_component.py
