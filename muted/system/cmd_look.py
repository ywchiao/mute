
from __future__ import annotations

from typing import List
from typing import Type

from component.exit import Exit
from component.role import Role
from component.room import Room

from event.event import Event
from message.message import Message
from system.channel import Channel

from logcat.logcat import LogCat

class CmdLook:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        servant.on(Event.CMD_LOOK, self._on_cmd_look)
        servant.on(Event.CMD_ABBR_LOOK, self._on_cmd_look)

    @LogCat.log_func
    def _on_cmd_look(
        self, e: Event, entity: str = '', args: List[str] = []
    ) -> None:
        role = Role.instance(entity)

        if not args:
            room = Room.instance(role.room)

            text = f'{room.name} -'
            Channel.toRole(entity, Message.TEXT, text)

            for text in room.description:
                Channel.toRole(entity, Message.TEXT, text)

            exits = Exit.instance(role.room)

            if not exits:
                text = '這裡沒有出口'
            else:
                text = f'  這裡明顯的出口有：{exits.keys()}'
        else:
            text = f'你在看什麼？'

        Channel.toRole(entity, Message.TEXT, text)

# cmd_look.py
