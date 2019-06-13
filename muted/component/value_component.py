
from component.component import Component

from logcat.logcat import LogCat

class ValueComponent(Component):
    def __init__(self, fname: str):
        super().__init__(fname)

    def update(self, entity: str, value: float) -> None:
        self._cache[entity] = value

    def value(self, entity: str) -> float:
        try:
            value = self._cache[entity]
            LogCat.log(f'ValueComponent.value entity: {entity} value: {value}')
        except KeyError:
            LogCat.log(f'ValueComponent.value entity: {entity} keyError')
            value = 0

        return value

# value_component.py
