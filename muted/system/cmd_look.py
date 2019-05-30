
from __future__ import annotations

from typing import List
from typing import Type

from component.description import Description
from component.exit import Exit
from component.name import Name
from component.npc import NPC
from component.passer import Passer
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
            text = [
                *self._room_desc(role.room),
                self._room_passer(role.room),
                self._room_exit(role.room)
            ]
        else:
            text = self._look_at(role.room, args[0])

        for line in text:
            Channel.to_role(entity, Message.TEXT, line)

    @LogCat.log_func
    def _look_at(self, room: str, tag: str) -> List[str]:
        target = Passer.instance(room).with_tag(tag)

        if target:
            text = [
                f'你上下打量著[{Name.instance(target).text}]，你看見一位：',
                *NPC.instance(target).description
            ]
        else:
            text = [f'  你在看什麼？']

        return text

    @LogCat.log_func
    def _room_desc(self, room: str) -> List[str]:
        room = Room.instance(room)

        return [
          f'{room.name} -',
          *room.description
        ]

    @LogCat.log_func
    def _room_exit(self, room: str) -> str:
        exits = Exit.instance(room)

        if not exits:
            text = f'  這裡沒有出口'
        else:
            text = f'  這裡明顯的出口有：{exits.keys()}'

        return text

    @LogCat.log_func
    def _room_passer(self, room: str) -> str:
        text = Passer.instance(room).list

        return f'  這裡旳人有：{text}'

# cmd_look.py
