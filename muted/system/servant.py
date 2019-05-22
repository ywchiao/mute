
from __future__ import annotations

from event.event import Event
from event.handler import Handler
from message.message import Message

from system.cmd_look import CmdLook
from system.cmd_say import CmdSay
from system.sign_in import SignIn

from logcat.logcat import LogCat

class Servant(Handler):
    _instance: Servant = None

    @LogCat.log_func
    def __init__(self):
        super().__init__()

        self.on(Message.TEXT, self._on_text)

    @classmethod
    def instance(cls) -> Servant:
        if not cls._instance:
            cls._instance = Servant()

            CmdLook(cls._instance)
            CmdSay(cls._instance)
            SignIn(cls._instance)

        return cls._instance

    @LogCat.log_func
    def _on_text(self, e: Event, entity: str, who: str, text: str) -> None:
        words = text.split()

        Event.trigger(
            Event(words[0], self, entity=entity, args=words[1:])
        )

# servant.py
