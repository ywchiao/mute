
from __future__ import annotations

from typing import List
from typing import Type

from component.name import Name
from component.role import Role
from component.atk_power import AtkPower
from component.atr_str import AtrStr
from component.def_power import DefPower
from component.exp_point import ExpPoint
from component.hit_point import HitPoint
from component.level import Level

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
        self, e: Event, entity: str = '', args: List[str] = []
    ) -> None:
        score = [
            f'你目前的狀態是：',
            f'  姓名：{Name.instance(entity).text}',
            f'  等級：{Level.instance(entity).value}',
            f'  攻擊力：{AtkPower.instance(entity).value}',
            f'  防禦力：{DefPower.instance(entity).value}',
            f'  血量：{HitPoint.instance(entity).value}/{HitPoint.instance(entity).max_value}',
            f'  經驗值：{ExpPoint.instance(entity).value}'
        ]

        for text in score:
            Channel.to_role(entity, Message.TEXT, text)

# cmd_score.py
