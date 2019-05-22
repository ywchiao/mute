
from __future__ import annotations

from typing import Type

from component.name import Name
from component.role import Role
from component.room import Room

from event.event import Event
from message.message import Message
from message.out_stream import OutStream

from logcat.logcat import LogCat

class SignIn:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        self._servant = servant

        servant.on(Message.SIGN_IN, self._on_sign_in)
        servant.on(Event.RECEPTION, self._on_reception)

    @LogCat.log_func
    def _on_reception(self, e: Event, entity: str) -> None:
        outs = OutStream.instance(entity)

        outs.append(
            Message(
                Message.TEXT, who='MUTED',
                text=f'歡迎來到 MUTE: Multi-User Texting Environment'
            )
        )

        outs.append(
            Message(Message.SIGN_IN, who='MUTED')
        )

    @LogCat.log_func
    def _on_sign_in(
        self, e: Event, entity: str, user_id: str = '', passwd: str = ''
    ) -> None:
        role = Role.instance(user_id, name=user_id)

        Name.instance(entity, name=role.name)
        Room.instance(role.room).enter(entity)

        OutStream.instance(entity).append(
            Message(
                Message.SYSTEM,
                who='MUTE',
                text=f'歡迎來到 MUTE: Multi-User Texting Environment'
            )
        )

        Event.trigger(Event(Event.CMD_LOOK, self._servant, entity=entity))

# sign_in.py
