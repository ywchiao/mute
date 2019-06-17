
from __future__ import annotations

from typing import List

from tools.block import Block

class Grid:
    def __init__(self, width: int, height: int):
        self._height = height
        self._width = width

        self._map: List[Block] = [
            Block.BLOCK for x in range(width * height)
        ]

    def cell(self, x: int, y: int) -> Block:
        return self._map[ x + y * self.width ]

    def update(self, x: int, y: int, value: Block) -> None:
        self._map[ x + y * self.width ] = value

    def __repr__(self) -> str:
        return '\n'.join([
            ''.join([
                self._map[ x + y * self.width ].value
                for x in range(self.width)
            ]).rstrip()
            for y in range(self.height)
        ])

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

# grid.py
