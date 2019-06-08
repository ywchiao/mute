
from __future__ import annotations

from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple

import json

from random import randint

class Seeking(NamedTuple):
    start: int
    fixed: int
    step: int
    vertical: bool

class Vertex(NamedTuple):
    x: int
    y: int

class Node:
    """A node class for A* Pathfinding"""
    def __init__(
        self, vertex: Vertex, parent: Optional[Node] = None
    ):
        self._parent = parent
        self._vertex = vertex

        self._g = parent.g + 1 if parent else 0
        self._h = 0

    @property
    def f(self):
        return self._g + self._h

    @property
    def g(self) -> int:
        return self._g

    @property
    def h(self) -> int:
        return self._h

    @h.setter
    def h(self, h: int) -> None:
        self._h = h

    @property
    def parent(self) -> Node:
        return self._parent

    @property
    def vertex(self) -> Vertex:
        return self._vertex

    @property
    def x(self) -> int:
        return self._vertex.x

    @property
    def y(self) -> int:
        return self._vertex.y

    def __eq__(self, other: Node) -> bool:
        return self.vertex == other.vertex

class Atlas(Facet):
    DATA_PATH = 'None'
    _cache = {}

    def __self__(self):
        pass

    def zone_map(self, entity: str) -> ZoneMap:
        if not entity in self._cache:
            self._cache[entity] = ZoneMap()

        return self._cache[entity]

if __name__ == '__main__':
    zone = Zone(17, 13)

    print(zone)

# atlas.py
