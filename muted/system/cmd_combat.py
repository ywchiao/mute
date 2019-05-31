
from __future__ import annotations

from typing import List
from typing import Type

from component.genus import Genus
from component.name import Name
from component.passer import Passer
from component.role import Role
from event.event import Event
from message.message import Message
from system.attack import Attack
from system.channel import Channel

from logcat.logcat import LogCat

class CmdCombat:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        self._servant = servant

        servant.on(Event.CMD_KILL, self._on_cmd_combat)
        servant.on(Event.CMD_ABBR_KILL, self._on_cmd_combat)

    @LogCat.log_func
    def _on_cmd_combat(
        self, e: Event, entity: str = '', args: List[str] = []
    ) -> None:
        role = Role.instance(entity)

        if not args:
            text = f'  你想要殺誰？'
        else:
            target = Passer.instance(role.room).with_tag(args[0])

            if not target:
                text = f'  這裡沒有這個人。'
            else:
                name = Name.instance(Genus.instance(target)).text
                text = f'  你大喝一聲：「{name}納命來。」就朝{name}發起攻擊。'

                Attack.instance().enlist(entity, target)

        Channel.to_role(entity, Message.TEXT, text)

# cmd_combat.py
