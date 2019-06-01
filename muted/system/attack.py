
from __future__ import annotations

from typing import List
from typing import Tuple

import random
import time

from component.atk_power import AtkPower
from component.genus import Genus
from component.hit_point import HitPoint
from component.name import Name
from event.event import Event

from message.message import Message
from system.channel import Channel
from system.regen import Regen

from logcat.logcat import LogCat

class Attack:
    _instance: Attack = None

    @LogCat.log_func
    def __init__(self):
        self._queue: List[Tuple(str, str, int)] = []

    @classmethod
    def instance(cls) -> Attack:
        if not cls._instance:
            cls._instance = Attack()

        return cls._instance

    @LogCat.log_func
    def enlist(self, attacker: str, defender: str) -> None:
        self._queue.append((attacker, defender, time.time_ns()))
        self._queue.append((defender, attacker, time.time_ns()))

#        self._attack(attacker, defender)

    def update(self, t_ns: int) -> None:
        queue = []

        for a, d, t in self._queue:
            if t_ns - t > 1500000000:
                self._attack(a, d)

                if HitPoint.instance(a).value and HitPoint.instance(d).value:
                    queue.append((a, d, t + 1500000000))
            else:
                queue.append((a, d, t))

        self._queue = queue

    def _attack(self, attacker: str, defender: str) -> bool:
        damage = random.randint(1, AtkPower.instance(attacker).value)
        HitPoint.instance(defender).lose(damage)

        Channel.to_role(
            attacker,
            Message.TEXT,
            f'  你對[{Name.instance(Genus.instance(defender)).text}]'
            f'的普通攻擊造成了{damage}點傷害。'
        )

        Channel.to_role(
            defender,
            Message.TEXT,
            f'  [{Name.instance(Genus.instance(attacker)).text}]'
            f'對你的普通攻擊造成了{damage}點傷害。'
        )

        if not HitPoint.instance(defender).value:
            Channel.to_role(
                attacker,
                Message.TEXT,
                f'  [{Name.instance(Genus.instance(defender)).text}]被'
                f'[{Name.instance(Genus.instance(attacker)).text}]殺死了。'
            )

            Channel.to_role(
                defender,
                Message.TEXT,
                f'  [{Name.instance(Genus.instance(defender)).text}] 被'
                f'[{Name.instance(Genus.instance(attacker)).text}] 殺死了。'
            )

#            Event.trigger(
#                Event(
#                    Event.DEATH, Servant.instance(),
                    #entity=defender
#                )
#            )

            Regen.instance().enlist(HitPoint.instance(attacker))

# attack.py
