
from __future__ import annotations

from typing import Mapping

from component.component import Component

class TextComponent(Component):
    def __init__(self, fname: str):
        super().__init__(fname)

    def text(self, entity: str) -> str:
        try:
            text = self._cache[entity]
        except KeyError:
            text = ""

        return text

    def update(self, entity: str, value: str) -> None:
        self._cache[entity] = value

# text_component.py
