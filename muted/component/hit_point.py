
import math

from component.stats import Stats

from logcat.logcat import LogCat

class HitPoint:
    BASE: int = 31
    R: float = 1.047
    HOT_DEFAULT: int = 5

    @staticmethod
    def max(entity: str) -> int:
        level = Stats.value('level', entity)

        return 10 * math.floor(
            HitPoint.BASE * math.pow(HitPoint.R, level - 1)
        )

    @staticmethod
    def update(entity: str, value: int) -> int:
        return Stats.update_value('hit_point', entity, value)

    @staticmethod
    def value(entity: str) -> int:
        return Stats.value('hit_point', entity)

# hit_point.py
