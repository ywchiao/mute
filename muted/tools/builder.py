
from __future__ import annotations

from typing import List
from typing import Mapping
from typing import Tuple

from pathlib import Path

from random import randint

from component.stats import Stats

from entity.entity import Entity

from tools.block import Block
from tools.building import Building
from tools.facing import Facing
from tools.grid import Grid
from tools.vertex import Vertex

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

    def __init__(self, width: int, height: int):
        self._map = Grid(width, height)

        self._buildings: List[Building] = []
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

        self._fix_building(width, height)
        self._fix_street()
        self._fix_road(width, height)
        self._fix_facing()

    def mini_map(self) -> str:
        return str(self)

    def publish(self) -> None:
        cache: Mapping[str, dict] = {}

        for x in range(0, self._map.width):
            for y in range(0, self._map.height):
                if not self._map.empty(x, y):
                    entity = Entity.eid()
                    cache[f'{x}x{y}'] = {
                        'entity': entity,
                        'vertex': Vertex(x, y)
                    }

                    Stats.update_text(
                        'room',
                        entity,
                        Stats.text(
                            'entity', 
                            self._map.cell(x, y).name.lower()
                        )
                    )

        for c in cache.values():
            exits = {}

            entity = c['entity']
            vertex = c['vertex']

            block = self._map.cell(vertex.x, vertex.y)

            if block in (
                Block.STREET_V,
                Block.CROSSROAD,
                Block.CORNER_SW,
                Block.CORNER_SE,
                Block.T_BOTTOM,
                Block.T_LEFT,
                Block.T_RIGHT
            ):
                if vertex.y > 0:
                    exits['n'] = cache[f'{vertex.x}x{vertex.y - 1}']['entity']

            if block in (
                Block.STREET_V,
                Block.CROSSROAD,
                Block.CORNER_NW,
                Block.CORNER_NE,
                Block.T_TOP,
                Block.T_LEFT,
                Block.T_RIGHT
            ):
                if vertex.y < self._map.height - 1:
                    exits['s'] = cache[f'{vertex.x}x{vertex.y + 1}']['entity']

            if block in (
                Block.STREET_H,
                Block.CROSSROAD,
                Block.CORNER_SW,
                Block.CORNER_NW,
                Block.T_TOP,
                Block.T_BOTTOM,
                Block.T_LEFT
            ):
                if vertex.x < self._map.width - 1:
                    exits['e'] = cache[f'{vertex.x + 1}x{vertex.y}']['entity']

            if block in (
                Block.STREET_H,
                Block.CROSSROAD,
                Block.CORNER_SE,
                Block.CORNER_NE,
                Block.T_TOP,
                Block.T_BOTTOM,
                Block.T_RIGHT
            ):
                if vertex.x > 0:
                    exits['w'] = cache[f'{vertex.x - 1}x{vertex.y}']['entity']

            Stats.update_text('exit', entity, exits)

        for b in self._buildings:
            if b.facing == Facing.EAST:
                exit = { 'e': cache[f'{b.x + 1}x{b.y}']['entity'] }
            elif b.facing == Facing.WEST:
                exit = { 'w': cache[f'{b.x - 1}x{b.y}']['entity'] }
            elif b.facing == Facing.NORTH:
                exit = { 'n': cache[f'{b.x}x{b.y - 1}']['entity'] }
            elif b.facing == Facing.SOUTH:
                exit = { 's': cache[f'{b.x}x{b.y + 1}']['entity'] }

            Stats.update_text('exit', cache[f'{b.x}x{b.y}']['entity'], exits)

        Stats.save('exit')
        Stats.save('room')

        f = Path(f'./tools/data/{Entity.eid()}.map')

        with f.open(mode='w', encoding='utf-8') as fout:
            fout.write(self.mini_map())

    def _check_facing(self, s: Vertex, d: Vertex) -> Facing:
        facing: Facing = Facing.NORTH

        if s.x > d.x:
            facing = Facing.WEST
        elif s.x < d.x:
            facing = Facing.EAST
        elif s.y > d.y:
            facing = Facing.NORTH
        else:
            facing = Facing.SOUTH

        return facing

    def _fix_building(self, w: int, h: int):
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
            self._buildings.append(Building(x, y, b))

    def _fix_corner_b2t(self, x: int, y: int) -> None:
        if self._map.empty(x - 1, y):
            if self._map.empty(x + 1, y):
                b = Block.STREET_V
            else:
                b = Block.CORNER_SW
        else:
            if self._map.empty(x + 1, y):
                b = Block.CORNER_SE
            else:
                b = Block.T_BOTTOM

        self._map.update(x, y, b)

    def _fix_corner_l2r(self, x: int, y: int) -> None:
        if self._map.empty(x, y - 1):
            if self._map.empty(x, y + 1):
                b = Block.STREET_H
            else:
                b = Block.CORNER_NW
        else:
            if self._map.empty(x, y + 1):
                b = Block.CORNER_SW
            else:
                b = Block.T_LEFT

        self._map.update(x, y, b)

    def _fix_corner_r2l(self, x: int, y: int) -> None:
        if self._map.empty(x, y - 1):
            if self._map.empty(x, y + 1):
                b = Block.STREET_H
            else:
                b = Block.CORNER_NE
        else:
            if self._map.empty(x, y + 1):
                b = Block.CORNER_SE
            else:
                b = Block.T_RIGHT

        self._map.update(x, y, b)

    def _fix_corner_t2b(self, x: int, y: int) -> None:
        if self._map.empty(x - 1, y):
            if self._map.empty(x + 1, y):
                b = Block.STREET_V
            else:
                b = Block.CORNER_NW
        else:
            if self._map.empty(x + 1, y):
                b = Block.CORNER_NE
            else:
                b = Block.T_TOP

        self._map.update(x, y, b)

    def _fix_facing(self):
        for b in self._buildings:
            if not b.facing == Facing.NORTH:
                block = self._map.cell(b.x, b.y - 1)

                if block == Block.CROSSROAD:
                    self._map.update(b.x, b.y - 1, Block.T_BOTTOM)
                elif block == Block.T_TOP:
                    self._map.update(b.x, b.y - 1, Block.STREET_H)

            if not b.facing == Facing.WEST:
                block = self._map.cell(b.x - 1, b.y)

                if block == Block.CROSSROAD:
                    self._map.update(b.x - 1, b.y, Block.T_RIGHT)
                elif block == Block.T_LEFT:
                    self._map.update(b.x - 1, b.y, Block.STREET_V)

            if not b.facing == Facing.SOUTH:
                block = self._map.cell(b.x, b.y + 1)

                if block == Block.CROSSROAD:
                    self._map.update(b.x, b.y + 1, Block.T_TOP)
                elif block == Block.T_BOTTOM:
                    self._map.update(b.x, b.y + 1, Block.STREET_H)

            if not b.facing == Facing.EAST:
                block = self._map.cell(b.x + 1, b.y)

                if block == Block.CROSSROAD:
                    self._map.update(b.x + 1, b.y, Block.T_LEFT)
                elif block == Block.T_RIGHT:
                    self._map.update(b.x + 1, b.y, Block.STREET_V)

    def _fix_hline(self, y: int, s: int, d: int) -> None:
        for x in range(s, d):
            if self._map.empty(x, y - 1):
                if self._map.empty(x, y + 1):
                    self._map.update(x, y, Block.STREET_H)
                else:
                    self._map.update(x, y, Block.T_TOP)
            else:
                if self._map.empty(x, y + 1):
                    self._map.update(x, y, Block.T_BOTTOM)
                else:
                    self._map.update(x, y, Block.CROSSROAD)

    def _fix_lane(self, path: List[Vertex]) -> None:
        u = path[0]

        for v in path[1:]:
            if v.x == u.x:
                self._map.update(v.x, v.y, Block.STREET_V)
            else:
                self._map.update(v.x, v.y, Block.STREET_H)

            u = v

    def _fix_path(self, path: List[Vertex]) -> None:
        u = path[0]

        for i in range(1, len(path) - 1):
            v = path[i]

            t = path[i + 1]

            if v.y > t.y:
                if v.x < u.x:
                    self._map.update(v.x, v.y, Block.CORNER_SW)
                elif v.x > u.x:
                    self._map.update(v.x, v.y, Block.CORNER_SE)
                else:
                    self._map.update(v.x, v.y, Block.STREET_V)
            elif v.y < t.y:
                if v.x < u.x:
                    self._map.update(v.x, v.y, Block.CORNER_NW)
                elif v.x > u.x:
                    self._map.update(v.x, v.y, Block.CORNER_NE)
                else:
                    self._map.update(v.x, v.y, Block.STREET_V)
            elif v.x < t.x:
                if v.y < u.y:
                    self._map.update(v.x, v.y, Block.CORNER_NW)
                elif v.y > u.y:
                    self._map.update(v.x, v.y, Block.CORNER_SW)
                else:
                    self._map.update(v.x, v.y, Block.STREET_H)
            elif v.x > t.x:
                if v.y < u.y:
                    self._map.update(v.x, v.y, Block.CORNER_NE)
                elif v.y > u.y:
                    self._map.update(v.x, v.y, Block.CORNER_SE)
                else:
                    self._map.update(v.x, v.y, Block.STREET_H)

            u = v

    def _fix_road(self, w: int, h: int) -> None:
        x = self._crossroads[0].x
        y = 0

        if randint(0, 1):
            while (
                self._map.cell(x, y) == Block.BLOCK and
                y < self._crossroads[0].y
            ):
                y += 1

            self._fix_corner_t2b(x, y)
            self._fix_vline(x, y + 1, h)
        else:
            y = h - 1

            while (
                self._map.cell(x, y) == Block.BLOCK and
                y > self._crossroads[1].y
            ):
                y -= 1

            self._fix_corner_b2t(x, y)
            self._fix_vline(x, 0, y)

        x = self._crossroads[1].x
        y = 0

        if randint(0, 1):
            while (
                self._map.cell(x, y) == Block.BLOCK and
                y < self._crossroads[0].y
            ):
                y += 1

            self._fix_corner_t2b(x, y)
            self._fix_vline(x, y + 1, h)
        else:
            y = h - 1

            while (
                self._map.cell(x, y) == Block.BLOCK and
                y > self._crossroads[1].y
            ):
                y -= 1

            self._fix_corner_b2t(x, y)
            self._fix_vline(x, 0, y)

        x = 0
        y = self._crossroads[0].y

        if randint(0, 1):
            while (
                self._map.cell(x, y) == Block.BLOCK and
                x < self._crossroads[0].x
            ):
                x += 1

            self._fix_corner_l2r(x, y)
            self._fix_hline(y, x + 1, w)
        else:
            x = w - 1

            while (
                self._map.cell(x, y) == Block.BLOCK and
                x > self._crossroads[1].x
            ):
                x -= 1

            self._fix_corner_r2l(x, y)
            self._fix_hline(y, 0, x)

        x = 0
        y = self._crossroads[1].y

        if randint(0, 1):
            while (
                self._map.cell(x, y) == Block.BLOCK and
                x < self._crossroads[0].x
            ):
                x += 1

            self._fix_corner_l2r(x, y)
            self._fix_hline(y, x + 1, w)
        else:
            x = w - 1

            while (
                self._map.cell(x, y) == Block.BLOCK and
                x > self._crossroads[1].x
            ):
                x -= 1

            self._fix_corner_r2l(x, y)
            self._fix_hline(y, 0, x)

    def _fix_street(self):
        for src in self._buildings:
            pathes = [
                self._map.find_path(src, dst) for dst in (
                    Vertex(src.x, self._crossroads[0].y),
                    Vertex(src.x, self._crossroads[1].y),
                    Vertex(self._crossroads[0].x, src.y),
                    Vertex(self._crossroads[1].x, src.y)
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

            path = pathes[index]

            self._fix_lane(path)
            src.facing = self._check_facing(path[0], path[1])
            self._fix_path(path)

    def _fix_vline(self, x: int, s: int, d: int) -> None:
        for y in range(s, d):
            if self._map.empty(x - 1, y):
                if self._map.empty(x + 1, y):
                    self._map.update(x, y, Block.STREET_V)
                else:
                    self._map.update(x, y, Block.T_LEFT)
            else:
                if self._map.empty(x + 1, y):
                    self._map.update(x, y, Block.T_RIGHT)
                else:
                    self._map.update(x, y, Block.CROSSROAD)

    def _on_axis(self, x: int, y: int) -> bool:
        on = True

        for v in self._crossroads:
            if x == v.x or y == v.y:
                break
        else:
            on = False

        return on

    def __repr__(self) -> str:
        return str(self._map)

if __name__ == '__main__':
    zone = Zone(19, 19)
    zone.publish()

    print(zone.mini_map())

# builder.py
