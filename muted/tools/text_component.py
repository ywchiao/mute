
from typing import Mapping
from typing import Sequence
from typing import Union

from component import Component

class TextComponent(Component):
    def __init__(self, data: Mapping[str, Union[str, Sequence[str]]] = {}):
        self._cache = data
        self._fname = 'text'

    def update(self, entity: str, value: Union[str, Sequence[str]]) -> None:
        self._cache[entity] = value

# text_component.py
