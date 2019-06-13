
from __future__ import annotations

from typing import Sequence
from typing import Type

from component.link import Link
from component.stats import Stats

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
        self, e: Event, entity: str = '', args: Sequence[str] = []
    ) -> None:
        role = Stats.text('binding', entity)
        at = Stats.text('at_room', role)
        exit = Stats.text('exit', at)

        try:
            room = exit[e.type[0]]

            Stats.list_remove('guest', at, Link(entity, role))
            Stats.update_text('at_room', role, room)
            Stats.list_append('guest', room, Link(entity, role))

            Event.trigger(Event(Event.CMD_LOOK, self._servant, entity=entity))
        except KeyError:
            Channel.to_role(entity, Message.TEXT, f'  這裡沒有出口')

# cmd_move.py
