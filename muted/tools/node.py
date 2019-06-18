
from __future__ import annotations

from typing import Optional

from tools.vertex import Vertex

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

# node.py
