
from __future__ import annotations

from typing import List

from tools.block import Block

class Grid:
    BLOCK: str = ' '
    STREET: str = '.'
    BLACKSMITH: str = 'S'
    HERBAL_SHOP: str = 'H'
    GROCERY_STORE: str = 'G'
    CLOTHING_STORE: str = 'C'
    INN: str = 'I'
    PAWN_SHOP: str = 'P'
    TAVERN: str = 'T'
    BANK: str = 'B'
    T_SHAPE: str = '-'
    CROSS: str = '+'
    NORTH: str = '^'
    SOUTH: str = 'v'
    EAST: str = '>'
    WEST: str = '<'

    PAVEMENT: str = '.+-'
    BUILDING: str = 'SHGCIPTB'
    GROUND: str = ' .+-'

    TAG: Map[str, str] = {
        '.': 'street',
        '+': 'cross',
        '-': 't_shape',
        'S': 'blacksmith',
        'G': 'grocery_store',
        'C': 'clothing_store',
        'I': 'inn',
        'B': 'bank',
        'P': 'pawn_shop',
        'T': 'tavern',
        'H': 'herbal_store'
    }

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

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

# grid.py
