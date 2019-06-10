
from __future__ import annotations

from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple

from  pathlib import Path
import json
import uuid

from random import randint

class Entity:
    @staticmethod
    def eid() -> str:
        return uuid.uuid4().hex

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

class Room:
    def __init__(self, tag: str):
        self._entity: str = Entity.eid()

        self._exit: Map[str, str] = {}

        self._desc = ''
        self._brief = ''
        self._name = ''
        self._tag = ''

    def add_exit(self, d: str, to: str) -> None:
        self._exit[d] = to

    @property
    def entity(self) -> str:
        return self._entity

    @property
    def vertex(self) -> Vertex:
        return self._vertex

class Zone:
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
        self._width = width
        self._height = height

        self._map: List[List[str]] = [
            [ Zone.BLOCK for x in range(width) ]
            for y in range(height)
        ]

        self._axis_x: Tuple[int, int] = (
            int(self._width * .33),
            int(self._width * .67)
        )

        self._axis_y: Tuple[int, int] = (
            int(self._height * .33),
            int(self._height * .67)
        )

        self._buildings: List[Node] = []
        self._facing: List[str] = []
        self._pavements: List[Vertex] = []

        self._fix_housing()
        self._fix_street()
        self._fix_road()
        self._fix_junction()

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

    def _seek_nonblock(self, seek: Seeking) -> int:
        index = seek.start

        try:
            if seek.vertical:
                while self._map[index][seek.fixed] == Zone.BLOCK:
                    index += seek.step
            else:
                while self._map[seek.fixed][index] == Zone.BLOCK:
                    index += seek.step
        except IndexError:
            pass

        return index

    def _count_links(self, vertex: Vertex) -> int:
        counts = 0

        for x, y in ((0, -1), (-1, 0), (0, 1), (1, 0)):
            try:
                if self._map[vertex.y + y][vertex.x + x] in Zone.PAVEMENT:
                    counts += 1
            except IndexError:
                pass

        return counts

    def _fix_housing(self):
        for t in range(0, len(Zone.BUILDING)):
            x = randint(int(self._width * .20), int(self._width * .80))
            y = randint(int(self._height * .20), int(self._height * .80))

            while (
                (not self._map[y][x] == Zone.BLOCK) or
                (x in self._axis_x) or
                (y in self._axis_y)
            ):
                x = randint(int(self._width * .20), int(self._width * .80))
                y = randint(int(self._height * .20), int(self._height * .80))

            self._map[y][x] = Zone.BUILDING[t]

            self._buildings.append(Node(Vertex(x, y)))

    def _fix_junction(self) -> None:
        for vertex in self._pavements:
            counts = self._count_links(vertex)

            if 4 == counts:
                self._map[vertex.y][vertex.x] = Zone.CROSS
            elif 3 == counts:
                self._map[vertex.y][vertex.x] = Zone.T_SHAPE

    def _fix_line(self, src: Vertex, dst: Vertex) -> None:
        if src.x == dst.x:
            for y in range(src.y, dst.y):
                self._map[y][src.x] = Zone.STREET
                self._pavements.append(Vertex(src.x, y))
        else:
            for x in range(src.x, dst.x):
                self._map[src.y][x] = Zone.STREET
                self._pavements.append(Vertex(x, src.y))

    def _fix_path(self, path: List[Vectex]) -> None:
        for x, y in path:
            self._map[y][x] = Zone.STREET

    def _fix_road(self) -> None:
        r = randint(0, 1)

        x = self._axis_x[r]
        y = min(
            self._seek_nonblock(Seeking(0, x, 1, True)),
            randint(int(self._height * .20), int(self._height * .25))
        )

        self._fix_line(Vertex(x, y), Vertex(x, self._height))

        x = self._axis_x[1 - r]
        y = max(
            self._seek_nonblock(Seeking(self._height - 1, x, -1, True)),
            randint(int(self._height * .75), int(self._height * .80))
        )

        self._fix_line(Vertex(x, 0), Vertex(x, y))

        r = randint(0, 1)

        y = self._axis_y[r]
        x = min(
            self._seek_nonblock(Seeking(0, y, 1, False)),
            randint(int(self._width * .20), int(self._width * .25))
        )

        self._fix_line(Vertex(x, y), Vertex(self._width, y))

        y = self._axis_y[1 - r]
        x = max(
            self._seek_nonblock(Seeking(self._width - 1, y, -1, False)),
            randint(int(self._width * .75), int(self._width * .80))
        )

        self._fix_line(Vertex(0, y), Vertex(x, y))

    def _fix_street(self):
        for src in self._buildings:
            pathes = [
                self.find(src, dst)
                for dst in (
                    Node(Vertex(src.x, self._axis_y[0])),
                    Node(Vertex(src.x, self._axis_y[1])),
                    Node(Vertex(self._axis_x[0], src.y)),
                    Node(Vertex(self._axis_x[1], src.y))
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

            self._fix_path(pathes[index][1:])

            if index < 2:
                if src.y < self._axis_y[index]:
                    self._facing.append(Zone.SOUTH)
                else:
                    self._facing.append(Zone.NORTH)
            else:
                if src.x < self._axis_x[index - 2]:
                    self._facing.append(Zone.EAST)
                else:
                    self._facing.append(Zone.WEST)

    def publish(self) -> None:
        cache: Map[str, Room] = {}

        for n in self._buildings:
            cache[f'{n.x}x{n.y}'] = Room(self._map[n.y][n.x])

        for v in self._pavement:
            cache[f'{v.x}x{v.y}'] = Room(self._map[v.y][v.x])

        for v in self._pavement:
            room = cache[f'{v.x}x{v.y}']

            for i, vec in (
                Vertex(0, -1), Vertex(-1, 0), Vertex(0, 1), Vertex(1, 0)
            ):
                x = v.x + vec.x
                y = v.y + vec.y

                if (
                    x < 0 or
                    x >= self._width or
                    y < 0 or
                    y >= self._height
                ):
                    continue

                if self._map[y][x] == Zone.BLOCK:
                    continue

                room.add_exit('nwse'[i], cache[f'{x}x{y}'].entity)

        for i, n in enumerate(self._building):
            room = cache[f'{n.x}x{n.y}']

            if self._facing[i] == '^':
                room.add_exit('n', cache[f'{n.x}x{n.y - 1}'].entity)
            elif self._facing[i] == '<':
                room.add_exit('w', cache[f'{n.x - 1}x{n.y}'].entity)
            elif self._facing[i] == 'v':
                room.add_exit('s', cache[f'{n.x}x{n.y + 1}'].entity)
            elif self._facing[i] == '>':
                room.add_exit('e', cache[f'{n.x + 1}x{n.y}'].entity)
            else:
                print(f'Panic! Facing error!')

    def __repr__(self) -> str:
        return '\n'.join([ ' '.join(street) for street in self._map ])

def to_spec():
    f = Path(f'./room.json')
    tf = Path(f'./text.json')
    vf = Path(f'./value.json')
    tgf = Path(f'./tag.json')

    print(f'------{f}-------')
    if f.is_file():
        spec = ''

        with f.open(encoding='utf-8') as fin:
            spec = json.load(fin)

            tag = {}

            for item in spec:
                for key, value in item.items():
                    if not 'entity' in value:
                        if type(value) in ( bool, float, int ):
                            item[key] = {
                                "entity": entity,
                                "value": value
                            }
                        else:
                            item[key] = {
                                "entity": entity,
                                "text": value
                            }

                tag[item['tag']['text']] = {}

                for key, value in item.items():
                    tag[item['tag']['text']][key] = item[key]['entity']

        with f.open(mode='w', encoding='utf-8') as fout:
            json.dump(spec, fout, ensure_ascii=False, indent=2)

        with tgf.open(mode='w', encoding='utf-8') as fout:
            json.dump(tag, fout, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    zone = Zone(27, 17)

    to_spec()

    print(zone)

# builder.py
