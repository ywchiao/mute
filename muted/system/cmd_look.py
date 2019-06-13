
from __future__ import annotations

from typing import List
from typing import Type

from component.stats import Stats

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
        role_id = Stats.text('binding', entity)
        room = Stats.text('at_room', role_id)

        if not args:
            text = [
                *self._room_desc(room),
                self._room_passer(room),
                self._room_exit(room)
            ]
        else:
            text = self._look_at(room, args[0])

        for line in text:
            Channel.to_role(entity, Message.TEXT, line)

    @LogCat.log_func
    def _look_at(self, room: str, tag: str) -> List[str]:
        target = Stats.text('entity', tag)

        if target:
            text = [
                f'你上下打量著[{Stats.text("name", target)}]，你看見：',
                *Stats.text('description', target)
            ]
        else:
            text = [f'  你在看什麼？']

        return text

    @LogCat.log_func
    def _room_desc(self, room: str) -> List[str]:
        room_type = Stats.text('room', room)

        return [
          f'{Stats.text("name", room_type)}',
          *Stats.text('description', room_type)
        ]

    @LogCat.log_func
    def _room_exit(self, room: str) -> str:
        exits = Stats.text('exit', room)

        if not exits:
            text = f'  這裡沒有出口'
        else:
            text = f'  這裡明顯的出口有：{", ".join(exits.keys())}'

        return text

    @LogCat.log_func
    def _room_passer(self, room: str) -> str:
        return ', '.join([
            f'{Stats.text("name", passer)} ({Stats.text("tag", passer)})'
            for passer in Stats.list_items('passer', room)
        ])

# cmd_look.py
