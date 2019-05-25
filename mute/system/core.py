
from __future__ import annotations

from event.event import Event
from event.handler import Handler
from message.message import Message

from window_manager.window_manager import WindowManager

from logcat.logcat import LogCat

class Core(Handler):
    _instance: Core = None

    @LogCat.log_func
    def __init__(self):
        super().__init__()

    @classmethod
    def instance(cls) -> Core:
        if not cls._instance:
            cls._instance = Core()

            WindowManager(cls._instance)

        return cls._instance

# core.py
