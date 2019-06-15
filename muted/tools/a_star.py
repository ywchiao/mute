
from __future__ import annotations

from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple

from pathlib import Path

from random import randint

import json

from component.text_component import TextComponent

from entity.entity import Entity

TEXT_COMPONENT = (
    'room',
    'exit'
)

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

class AStar:
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

    def __init__(self):
        self._map: List[List[str]] = [
            [ Zone.BLOCK for x in range(width) ]
            for y in range(height)
        ]

    def find_path(self, grid: Grid, src: Node, dst: Node) -> Sequence[Vertex]:
        openned: List[Node] = [ src ]
        closed: List[Node] = []

        while openned:
            node: Node = openned[0]
            index: int = 0

            for idx, current in enumerate(openned):
                if current.f < node.f:
                    node = current
                    index = idx

            openned.pop(index)
            closed.append(node)

            if node == dst:
                path: List[Vertex] = []
                current: Optional[Node] = node

                while current:
                    path.append(current.vertex)
                    current = current.parent

                return path[::-1] # Return reversed path

            for node in self._child_list(node):
                if self._has_visited(node, closed):
                    continue

                for current in openned:
                    if current == node and current.g >= node.g:
                        break
                else:
                    node.h = (
                        ((node.x - dst.x) ** 2) +
                        ((node.y - dst.y) ** 2)
                    )

                    openned.append(node)

    def _has_visited(self, node: Node, node_list: List[Node]) -> bool:
        visited: bool = True

        for current in node_list:
            if current == node:
                break
        else:
            visited = False

        return visited

    def _child_list(self, node: Node) -> Sequence[Node]:
        child_list: List[Node] = []

        for x_step, y_step in ((0, -1), (-1, 0), (0, 1), (1, 0)):
            x = node.x + x_step
            y = node.y + y_step

            if (
                x < 0 or
                x >= self._width or
                y < 0 or
                y >= self._height
            ):
                continue

            if not self._map[y][x] in Zone.GROUND:
                continue

            child_list.append(Node(Vertex(x, y), node))

        return child_list

# a_star.py
