
from __future__ import annotations

from typing import Type

from component.role import Role
from component.room import Room

from event.event import Event
from message.message import Message
from message.out_stream import OutStream

from logcat.logcat import LogCat

class CmdLook:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        servant.on(Event.CMD_LOOK, self._on_cmd_look)
        servant.on(Event.CMD_ABBR_LOOK, self._on_cmd_look)

    @LogCat.log_func
    def _on_cmd_look(
        self, e: Event, entity: str = '', args: str = ''
    ) -> None:
        role = Role.instance(entity)
        outs = OutStream.instance(entity)

        if not args:
            room = Room.instance(role.room)

            outs.append(
                Message(
                    Message.TEXT,
                    who='MUTE',
                    text=f'{room.name} -'
                )
            )

            for text in room.description:
                outs.append(
                    Message(
                        Message.TEXT,
                        who='MUTE',
                        text=text
                    )
                )

            if not room.exits:
                outs.append(
                    Message(
                        Message.TEXT,
                        who='MUTE',
                        text='這裡沒有出口'
                    )
                )
            else:
                outs.append(
                    Message(
                        Message.TEXT,
                        who='MUTE',
                        text=room.exits
                    )
                )

# cmd_look.py
