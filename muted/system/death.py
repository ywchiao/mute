
from __future__ import annotations

from typing import List
from typing import Type

from component.text_component import TextComponent

from event.event import Event
from message.message import Message
from system.channel import Channel

from logcat.logcat import LogCat

class Death:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        servant.on(Event.DEATH, self._on_death)

    @LogCat.log_func
    def _on_death(
        self, e: Event, entity: str = ''
    ) -> None:
        LogCat.log(f' ----------- ogt death event -=-----')

# death.py
