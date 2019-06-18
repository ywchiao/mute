
from __future__ import annotations

from tools.block import Block
from tools.facing import Facing

class Building:
    """A building class for A* Pathfinding"""
    def __init__(self, x: int, y: int, b: Block):
        self._b = b
        self._f = Facing.NORTH
        self._x = x
        self._y = y

    @property
    def block(self) -> Block:
        return self._b

    @property
    def facing(self) -> Facing:
        return self._f

    @facing.setter
    def facing(self, f: Facing) -> None:
        self._f = f

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

# building.py
