
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

class CmdMove:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        self._servant = servant

        servant.on(Event.CMD_EAST, self._on_cmd_move)
        servant.on(Event.CMD_ABBR_EAST, self._on_cmd_move)
        servant.on(Event.CMD_NORTH, self._on_cmd_move)
        servant.on(Event.CMD_ABBR_NORTH, self._on_cmd_move)
        servant.on(Event.CMD_SOUTH, self._on_cmd_move)
        servant.on(Event.CMD_ABBR_SOUTH, self._on_cmd_move)
        servant.on(Event.CMD_WEST, self._on_cmd_move)
        servant.on(Event.CMD_ABBR_WEST, self._on_cmd_move)

    @LogCat.log_func
    def _on_cmd_move(
        self, e: Event, entity: str = '', args: List[str] = []
    ) -> None:
        role = Role.instance(entity)
        exit = Exit.instance(role.room)

        room = exit.to(e.type[0])

        if None != room:
            Room.instance(role.room).leave(entity)
            Room.instance(room).enter(entity)

            role.enter(room)

            Event.trigger(Event(Event.CMD_LOOK, self._servant, entity=entity))
        else:
            Channel.to_role(entity, Message.TEXT, f'  這裡沒有出口')

# cmd_move.py
