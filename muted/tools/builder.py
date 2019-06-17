
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

from tools.block import Block
from tools.facing import Facing
from tools.grid import Grid
from tools.node import Node
from tools.vertex import Vertex

TEXT_COMPONENT = (
    'room',
    'exit'
)

class Seeking(NamedTuple):
    start: int
    fixed: int
    step: int
    vertical: bool

class Zone:
    BUILDING: Tuple[Block] = (
        Block.BANK,
        Block.BLACKSMITH,
        Block.CLOTHING_STORE,
        Block.GROCERY_STORE,
        Block.HERBAL_STORE,
        Block.INN,
        Block.PAWN_SHOP,
        Block.TAVERN,
        Block.MARTIAL_CLUB,
        Block.RESIDENCE,
        Block.PINBOARD,
        Block.WORKSHOP
    )

    GROUND: Tuple[Block] = (
        Block.BLOCK,
        Block.CROSSROAD,
        Block.STREET_H,
        Block.STREET_V,
        Block.T_RIGHT,
        Block.T_LEFT,
        Block.T_TOP,
        Block.T_BOTTOM
    )

    def __init__(self, width: int, height: int):
        self._map = Grid(width, height)

        self._components: Mapping[str, Type[Component]] = {}

        for component in TEXT_COMPONENT:
            self._components[component] = TextComponent.instance(component)

        self._entity_component = TextComponent.instance('entity')

        self._buildings: List[Node] = []
        self._facing: List[Facing] = []
        self._pavements: Mapping[str, Vertex] = {}
        self._crossroads: Tuple[Vertex] = (
            Vertex(
                randint(int(width * .29), int(width * .37)),
                randint(int(height * .29), int(height * .37))
            ),
            Vertex(
                randint(int(width * .61), int(width * .71)),
                randint(int(height * .61), int(height * .71))
            )
        )

        self._fix_road(width, height)
        self._fix_housing(width, height)
        self._fix_street()
        self._fix_line(width, height)

    def find(self, src: Node, dst: Node) -> Sequence[Vertex]:
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
                    path.append(Vertex(current.x, current.y))
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
                x >= self._map.width or
                y < 0 or
                y >= self._map.height
            ):
                continue

            if not self._map.cell(x, y) in Zone.GROUND:
                continue

            child_list.append(Node(Vertex(x, y), node))

        return child_list

    def _fix_housing(self, w: int, h: int):
        x = randint(int(w * .20), int(w * .80))
        y = randint(int(h * .20), int(h * .80))

        for b in Zone.BUILDING:
            while (
                not self._map.cell(x, y) == Block.BLOCK or
                self._on_axis(x, y)
            ):
                x = randint(int(w * .20), int(w * .80))
                y = randint(int(h * .20), int(h * .80))

            self._map.update(x, y, b)
            self._buildings.append(Node(Vertex(x, y)))

    def _on_axis(self, x: int, y: int) -> bool:
        on = True

        for v in self._crossroads:
            if x == v.x or y == v.y:
                break
        else:
            on = False

        return on

    def _fix_line(self, w: int, h: int) -> None:
        x = self._crossroads[0].x
        y = 0

        if self._map.cell(x, y) == Block.BLOCK:
            while self._map.cell(x, y) == Block.BLOCK:
                y += 1

            self._fix_corner_nw(x, y)
            self._fix_vline(x, y + 1, h)
        else:
            y = h - 1

            while self._map.cell(x, y) == Block.BLOCK:
                y -= 1

            self._fix_corner_sw(x, y)
            self._fix_vline(x, self._crossroads[0].y, y)

    def _fix_corner_nw(self, x: int, y: int) -> None:
        if self._map.cell(x - 1, y) == Block.BLOCK:
            if self._map.cell(x + 1, y) == Block.BLOCK:
                b = Block.T_TOP
            else:
                b = Block.CORNER_NW
        else:
            if self._map.cell(x + 1, y) == Block.BLOCK:
                b = Block.CORNER_NE
            else:
                b = Block.STREET_V

        self._map.update(x, y, b)

    def _fix_corner_sw(self, x: int, y: int) -> None:
        if self._map.cell(x - 1, y) == Block.BLOCK:
            if self._map.cell(x + 1, y) == Block.BLOCK:
                b = Block.T_BOTTOM
            else:
                b = Block.CORNER_SW
        else:
            if self._map.cell(x + 1, y) == Block.BLOCK:
                b = Block.CORNER_SE
            else:
                b = Block.STREET_V

        self._map.update(x, y, b)

    def _fix_hline(self, y: int, s: int, d: int) -> None:
        for x in range(s, d):
            if self._map.cell(x, y) == Block.BLOCK:
                self._map.update(x, y, Block.STREET_H)
            elif self._map.cell(x, y) == Block.STREET_V:
                self._map.update(x, y, Block.CROSSROAD)

    def _fix_vline(self, x: int, s: int, d: int) -> None:
        for y in range(s, d):
            if self._map.cell(x, y) == Block.BLOCK:
                self._map.update(x, y, Block.STREET_V)
            elif self._map.cell(x, y) == Block.STREET_H:
                self._map.update(x, y, Block.CROSSROAD)

    def _fix_path(self, path: List[Vertex]) -> None:
        u = path[0]

        for v in path[1:-1]:
            if v.x == u.x:
                self._map.update(v.x, v.y, Block.STREET_V)
            else:
                self._map.update(v.x, v.y, Block.STREET_H)

            self._pavements[f'{v.x}x{v.y}]'] = v

            u = v

        v = path[-1]
        block = None

        if u.x == v.x:
            if u.y < v.y:
                if self._map.cell(v.x, v.y) == Block.T_TOP:
                    block = Block.CROSSROAD
                else:
                    block = Block.T_BOTTOM
            else:
                if self._map.cell(v.x, v.y) == Block.T_BOTTOM:
                    block = Block.CROSSROAD
                else:
                    block = Block.T_TOP
        else:
            if u.x < v.x:
                if self._map.cell(v.x, v.y) == Block.T_LEFT:
                    block = Block.CROSSROAD
                else:
                    block = Block.T_RIGHT
            else:
                if self._map.cell(v.x, v.y) == Block.T_RIGHT:
                    block = Block.CROSSROAD
                else:
                    block = Block.T_LEFT

        self._map.update(v.x, v.y, block)

        self._pavements[f'{v.x}x{v.y}]'] = v

    def _fix_road(self, w: int, h: int) -> None:
        if randint(0, 1):
            self._fix_vline(self._crossroads[0].x, 0, self._crossroads[1].y)
            self._fix_vline(self._crossroads[1].x, self._crossroads[0].y, h)
        else:
            self._fix_vline(self._crossroads[0].x, self._crossroads[0].y, h)
            self._fix_vline(self._crossroads[1].x, 0, self._crossroads[1].y)

        if randint(0, 1):
            self._fix_hline(self._crossroads[0].y, 0, self._crossroads[1].x)
            self._fix_hline(self._crossroads[1].y, self._crossroads[0].x, w)
        else:
            self._fix_hline(self._crossroads[0].y, self._crossroads[0].x, w)
            self._fix_hline(self._crossroads[1].y, 0, self._crossroads[1].x)

    def _fix_crossroad(self, w: int, h: int) -> None:

        for x in vx:
            for y in vy:
                self._map.update(x, y, Block.CROSSROAD)

    def _fix_street(self):
        for src in self._buildings:
            pathes = [
                self.find(src, dst) for dst in (
                    Node(Vertex(src.x, self._crossroads[0].y)),
                    Node(Vertex(src.x, self._crossroads[1].y)),
                    Node(Vertex(self._crossroads[0].x, src.y)),
                    Node(Vertex(self._crossroads[1].x, src.y))
                )
            ]

            cost = len(pathes[0])
            index = 0

            for i, path in enumerate(pathes):
                if len(path) < cost:
                    cost = len(path)
                    index = i
                elif len(path) == cost:
                    index = index if randint(0, 1) else i

            self._fix_path(pathes[index])

#            if index < 2:
#                if src.y < self._axis_y[index]:
#                    self._facing.append(Facing.SOUTH)
#                else:
#                    self._facing.append(Facing.NORTH)
#            else:
#                if src.x < self._axis_x[index - 2]:
#                    self._facing.append(Facing.EAST)
#                else:
#                    self._facing.append(Facing.WEST)

    def publish(self) -> None:
        cache: Mapping[str, str] = {}
        room_component = self._components['room']
        exit_component = self._components['exit']

        for n in (*self._buildings, *self._pavements.values()):
            entity = Entity.eid()
            cache[f'{n.x}x{n.y}'] = entity
            room_component.update(
                entity,
                self._entity_component.text(
                    self._map.cell(n.x, n.y).name.lower()
                )
            )

        for v in self._pavements.values():
            exits = {}

            for i, vec in enumerate((
                Vertex(0, -1), Vertex(-1, 0), Vertex(0, 1), Vertex(1, 0)
            )):
                x = v.x + vec.x
                y = v.y + vec.y

                if (
                    x < 0 or
                    x >= self._map.width or
                    y < 0 or
                    y >= self._map.height
                ):
                    continue

                if self._map.cell(x, y) == Block.BLOCK:
                    continue

                try:
                    exits['nwse'[i]] = cache[f'{x}x{y}']
                except KeyError:
                    print(f'KeyError: x {x} y {y} {"nwse"[i]} {self._map.cell(x, y).name}')

            exit_component.update(cache[f'{v.x}x{v.y}'], exits)

        for i, n in enumerate(self._buildings):
            room = cache[f'{n.x}x{n.y}']

#            if self._facing[i] == '^':
#                exit_component.update(
#                    room,
#                    { 'n': cache[f'{n.x}x{n.y - 1}'] }
                #)
#            elif self._facing[i] == '<':
#                exit_component.update(
#                    room,
#                    { 'w': cache[f'{n.x - 1}x{n.y}'] }
#                )
#            elif self._facing[i] == 'v':
#                exit_component.update(
#                    room,
#                    { 's': cache[f'{n.x}x{n.y + 1}'] }
#                )
#            elif self._facing[i] == '>':
#                exit_component.update(
#0                    room,
#                    { 'e': cache[f'{n.x + 1}x{n.y}'] }
#                )
#            else:
#                print(f'Panic! Facing error!')

#        for key, value in self._components.items():
#            value.save(key)

    def mini_map(self) -> str:
        return str(self)

    def __repr__(self) -> str:
        return str(self._map)

if __name__ == '__main__':
    zone = Zone(19, 19)
    zone.publish()

    print(zone.mini_map())
    print(f'01234567890123456789012345')
    print(f'0         1         2')

# builder.py
