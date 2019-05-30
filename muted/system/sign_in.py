
from __future__ import annotations

from typing import Type

from component.name import Name
from component.role import Role
from component.room import Room

from event.event import Event
from message.message import Message
from system.channel import Channel

from logcat.logcat import LogCat

class SignIn:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        self._servant = servant

        servant.on(Message.SIGN_IN, self._on_sign_in)
        servant.on(Event.RECEPTION, self._on_reception)

    @LogCat.log_func
    def _on_reception(self, e: Event, entity: str) -> None:
        text=f'歡迎來到 MUTE: Multi-User Texting Environment'
        Channel.to_role(entity, Message.TEXT, text)

        Channel.ask_role(entity, Message.SIGN_IN)

    @LogCat.log_func
    def _on_sign_in(
        self, e: Event, entity: str, user_id: str = '', passwd: str = ''
    ) -> None:
        role = Role.instance(user_id, name=user_id)

        Name.instance(entity, name=role.name)
        Room.instance(role.room).enter(entity)

        text = f'歡迎來到 MUTE: Multi-User Texting Environment'
        Channel.to_role(entity, Message.SYSTEM, text)

        Event.trigger(Event(Event.CMD_LOOK, self._servant, entity=entity))

# sign_in.py
