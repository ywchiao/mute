
from __future__ import annotations

import random

from component.hit_point import HitPoint
from component.link import Link
from component.stats import Stats

from event.event import Event

from message.message import Message
from system.channel import Channel
from system.heal_over_time import HealOverTime
from system.timed_task import TimedTask

from logcat.logcat import LogCat

class Attack:
    TICK_NORMAL: float = 1.5

    @LogCat.log_func
    def __init__(self, attacker: Link, defender: Link):
        self._attacker = attacker
        self._defender = defender

    def update(self) -> bool:
        attacker = self._attacker
        defender = self._defender

        damage = random.randint(1, Stats.attack_power(attacker.role))

        hp = HitPoint.value(defender.role) - damage
        HitPoint.update(defender.role, hp if hp > 0 else 0)

        if not HitPoint.value(defender.role):
            if attacker.entity:
                Channel.to_role(
                    attacker.entity,
                    Message.TEXT,
                    f'  [{Stats.text("name", defender.role)}]被'
                    f'[{Stats.text("name", attacker.role)}] 殺死了。'
                )

            if defender.entity:
                Channel.to_role(
                    defender.entity,
                    Message.TEXT,
                    f'  [{Stats.text("name", defender.role)}]被'
                    f'[{Stats.text("name", attacker.role)}] 殺死了。'
                )

            TimedTask.schedule(
                HealOverTime(attacker.role, HealOverTime.HEAL_DEFAULT),
                HealOverTime.TICK_NORMAL
            )
        else:
            if attacker.entity:
                Channel.to_role(
                    attacker.entity,
                    Message.TEXT,
                    f'  你對[{Stats.text("name", defender.role)}]'
                    f'的普通攻擊造成了 {damage}點傷害。'
                )

            if defender.entity:
                Channel.to_role(
                    defender.entity,
                    Message.TEXT,
                    f'  [{Stats.text("name", attacker.role)}]'
                    f'對你的普通攻擊造成了 {damage}點傷害。'
                )

        return not (
            HitPoint.value(defender.role) and HitPoint.value(attacker.role)
        )

# attack.py
