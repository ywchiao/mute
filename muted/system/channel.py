
from __future__ import annotations

from component.room import Room

from message.message import Message
from message.out_stream import OutStream

class Channel:
    @staticmethod
    def askRole(entity: str, type_: str) -> None:
        OutStream.instance(entity).append(
            Message(type_, who='MUTED')
        )

    @staticmethod
    def toRole(entity: str, type_: str, text: str = '') -> None:
        OutStream.instance(entity).append(
            Message(type_, who='MUTED', text=text)
        )

    @staticmethod
    def toRoom(entity: str, type_: str, text: str='') -> None:
        for guest in Room.instance(entity).guests:
            Channel.toRole(guest, type_, text)

# channel.py
