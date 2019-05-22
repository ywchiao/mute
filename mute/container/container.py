
from __future__ import annotations

from element.element import Element

from logcat.logcat import LogCat

class Container(Element):
    def __init__(self, x=0, y=0, width=1, height=1):
        super().__init__(x, y, width, height)

        self._elements = []

    @LogCat.log_func
    def add(self, element) -> Container:
        self._elements.append(element)

        return self

    @property
    def elements(self):
        return self._elements

# container.py
