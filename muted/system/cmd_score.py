
from __future__ import annotations

from typing import Sequence
from typing import Type

from component.hit_point import HitPoint
from component.stats import Stats

from event.event import Event
from message.message import Message
from system.channel import Channel

from logcat.logcat import LogCat

class CmdScore:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        servant.on(Event.CMD_SCORE, self._on_cmd_score)
        servant.on(Event.CMD_ABBR_SCORE, self._on_cmd_score)

    @LogCat.log_func
    def _on_cmd_score(
        self, e: Event, entity: str = '', args: Sequence[str] = []
    ) -> None:
        role = Stats.text('binding', entity)

        score = [
            f'你目前的狀態是：',
            f'  姓名：{Stats.text("name", role)}',
            f'  等級：{Stats.value("level", role)}',
            f'  攻擊力：{Stats.attack_power(role)}',
            f'  防禦力：{Stats.defence_power(role)}',
            f'  血量：{HitPoint.value(role)}/{HitPoint.max(role)}',
            f'  經驗值：{Stats.value("exp_point", role)}/(...)'
        ]

        for text in score:
            Channel.to_role(entity, Message.TEXT, text)

# cmd_score.py
