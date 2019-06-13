
from __future__ import annotations

from typing import Sequence
from typing import Type

from event.event import Event
from message.message import Message
from system.channel import Channel

from logcat.logcat import LogCat

class CmdEcho:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        servant.on(Event.CMD_ECHO, self._on_cmd_echo)

    @LogCat.log_func
    def _on_cmd_echo(
        self, e: Event, entity: str = '', args: Sequence[str] = []
    ) -> None:
        text = f'ECHO 說：{" ".join(args)}'

        Channel.to_role(entity, Message.TEXT, text)

# cmd_echo.py
