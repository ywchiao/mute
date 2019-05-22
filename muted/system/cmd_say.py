
from __future__ import annotations

from typing import Type

from component.name import Name
from component.role import Role
from component.room import Room

from event.event import Event
from message.message import Message
from message.out_stream import OutStream

from logcat.logcat import LogCat

class CmdSay:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        servant.on(Event.CMD_SAY, self._on_cmd_say)

    @LogCat.log_func
    def _on_cmd_say(
        self, e: Event, entity: str = '', args: str = ''
    ) -> None:
        role = Role.instance(entity)

        if not args:
            OutStream.instance(entity).append(
                Message(
                    Message.TEXT,
                    who='MUTE',
                    text=f'你想說什麼？'
                )
            )
        else:
            text = f'{Name.instance(entity).text}說：{" ".join(args)}'

            for entity in Room.instance(role.room).guests:
                OutStream.instance(entity).append(
                    Message(
                        Message.TEXT,
                        who='MUTE',
                        text=text
                    )
                )

# cmd_say.py
