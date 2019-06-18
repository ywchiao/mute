
from __future__ import annotations

from typing import List
from typing import Optional
from typing import Tuple

from tools.node import Node
from tools.vertex import Vertex

class AStar:
    def find_path(self, src: Vertex, dst: Vertex) -> Tuple[Vertex]:
        openned: List[Node] = [ Node(src) ]
        closed: List[Node] = []
        path: List[Vertex] = []

        while openned:
            node: Node = openned[0]
            index: int = 0

            for i, n in enumerate(openned):
                if n.f < node.f:
                    node = n
                    index = i

            openned.pop(index)
            closed.append(node)

            if node.vertex == dst:
                break

            for node in [
                Node(v, node)
                for v in self.near_cells(node.x, node.y)
                if self.empty(v.x, v.y) or self.passable(v.x, v.y)
            ]:
                if self._has_visited(node, closed):
                    continue

                for n in openned:
                    if n.vertex == node.vertex and n.g >= node.g:
                        break
                else:
                    node.h = (
                        ((node.x - dst.x) ** 2) +
                        ((node.y - dst.y) ** 2)
                    )

                    openned.append(node)

        node: Optional[Node] = closed[-1]

        while node:
            path.append(node.vertex)
            node = node.parent

        path.reverse()

        return tuple(path)

    def _has_visited(self, node: Node, node_list: List[Node]) -> bool:
        visited: bool = True

        for n in node_list:
            if n.vertex == node.vertex:
                break
        else:
            visited = False

        return visited

# a_star.py
