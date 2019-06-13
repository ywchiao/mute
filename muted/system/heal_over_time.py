
from component.hit_point import HitPoint

class HealOverTime:
    HEAL_DEFAULT: int = 5
    TICK_NORMAL: int = 5

    def __init__(self, entity: str, heal: int):
        self._entity = entity
        self._heal = heal

    def update(self) -> bool:
        hp = HitPoint.value(self._entity) + self._heal
        max_hp = HitPoint.max(self._entity)

        HitPoint.update(self._entity, hp if hp < max_hp else max_hp)

        return hp >= max_hp

# heal_over_time.py
