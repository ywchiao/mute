
from __future__ import annotations

from typing import List

from tools.a_star import AStar
from tools.block import Block
from tools.block import PASSABLE
from tools.vertex import Vertex

class Grid(AStar):
    def __init__(self, width: int, height: int):
        self._height = height
        self._width = width

        self._map: List[Block] = [
            Block.BLOCK for x in range(width * height)
        ]

    def cell(self, x: int, y: int) -> Optional[Block]:
        block = None

        if x >= 0 and  y >= 0 and x < self.width and y < self.height:
            block = self._map[ x + y * self.width ]

        return block

    def empty(self, x: int, y: int) -> bool:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        else:
            return self._map[ x + y * self.width ] == Block.BLOCK

    def passable(self, x: int, y: int) -> bool:
        return self._map[ x + y * self.width ] in PASSABLE

    def update(self, x: int, y: int, value: Block) -> None:
        self._map[ x + y * self.width ] = value

    def near_blocks(self, x: int, y: int) -> Tuple[Block]:
        return tuple([
            self.cell(v.x, v.y) for v in self.near_cells(x, y)
        ])

    def near_cells(self, x: int, y: int) -> Tuple[Vertex]:
        return tuple([
            Vertex(x + x_offset, y + y_offset)
            for x_offset, y_offset in ((0, -1), (-1, 0), (0, 1), (1, 0))
            if self.cell(x + x_offset, y + y_offset)
        ])

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
