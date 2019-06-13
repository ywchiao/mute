
from __future__ import annotations

from component.list_component import ListComponent
from component.text_component import TextComponent
from component.value_component import ValueComponent

class Stats:
    @staticmethod
    def attack_power(entity: str) -> int:
        return (
            Stats.value('attack_power', entity) +
            Stats.value('strength', entity)
        )

    @staticmethod
    def defence_power(entity: str) -> int:
        return Stats.value('defence_power', entity)

    @staticmethod
    def exp_point(entity: str) -> int:
        return Stats.value('exp_point', entity)

    @staticmethod
    def text(component: str, entity: str) -> str:
        return TextComponent.instance(component).text(entity)

    @staticmethod
    def value(component: str, entity: str) -> int:
        return ValueComponent.instance(component).value(entity)

    @staticmethod
    def list_append(component: str, entity: str, value: str) -> None:
        ListComponent.instance(component).append(entity, value)

    @staticmethod
    def list_items(component: str, entity: str) -> Sequence[str]:
        return ListComponent.instance(component).items(entity)

    @staticmethod
    def list_remove(component: str, entity: str, value: str) -> None:
        ListComponent.instance(component).remove(entity, value)

    @staticmethod
    def update_text(component: str, entity: str, value: str) -> None:
        TextComponent.instance(component).update(entity, value)

    @staticmethod
    def update_value(component: str, entity: str, value: float) -> None:
        ValueComponent.instance(component).update(entity, value)

# stats.py
