
from __future__ import annotations

from typing import Sequence
from typing import Type

from component.stats import Stats

from event.event import Event
from message.message import Message
from system.channel import Channel

from logcat.logcat import LogCat

class CmdSay:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        servant.on(Event.CMD_SAY, self._on_cmd_say)

    @LogCat.log_func
    def _on_cmd_say(
        self, e: Event, entity: str = '', args: Sequence[str] = []
    ) -> None:
        if not args:
            text = f'  你想說什麼？'

            Channel.to_role(entity, Message.TEXT, text)
        else:
            role = Stats.text('binding', entity)
            room = Stats.text('at_room', role)

            text = f'{Stats.text("name", role)} ({Stats.text("tag", role)}) 說：{" ".join(args)}'

            Channel.to_room(room, Message.TEXT, text)

# cmd_say.py
