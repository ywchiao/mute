
from __future__ import annotations

import socket

from event.event import Event
from event.handler import Handler
from system.net_io import NetIO
from system.timed import Timed

from logcat.logcat import LogCat

class Muted(Handler):
    @LogCat.log_func
    def __init__(self):
        super().__init__()

        self._net_io = None

    @LogCat.log_func
    def start(self):
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as server_socket:
            self._net_io = NetIO(server_socket)

            self._loop()

    def _bootstrap(self) -> None:
        pass

    def _loop(self) -> None:
        while True:
            self._net_io.check()

            while Event.ready():
                e = Event.next()

                if e.target:
                    e.target.on_event(e)
                else:
                    self.on_event(e)

            Timed.update()

if __name__ == '__main__':
    muted = Muted()

    muted.start()

# muted.py
