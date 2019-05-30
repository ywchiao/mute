
from __future__ import annotations

from component.room import Room

from message.message import Message
from message.out_stream import OutStream

class Channel:
    @staticmethod
    def ask_role(entity: str, type_: str) -> None:
        OutStream.instance(entity).append(
            Message(type_, who='MUTED')
        )

    @staticmethod
    def to_role(entity: str, type_: str, text: str = '') -> None:
        OutStream.instance(entity).append(
            Message(type_, who='MUTED', text=text)
        )

    @staticmethod
    def to_room(entity: str, type_: str, text: str='') -> None:
        for guest in Room.instance(entity).guests:
            Channel.to_role(guest, type_, text)

# channel.py
