
from __future__ import annotations

from component.stats import Stats

from message.message import Message
from message.out_stream import OutStream

from logcat.logcat import LogCat

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
        for guest in Stats.list_items('guest', entity):
            Channel.to_role(guest.entity, type_, text)

# channel.py
