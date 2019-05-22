
from __future__ import annotations

import socket

from facet.facet import Facet
from message.message import Message

from logcat.logcat import LogCat

class OutStream(Facet):
    DATA_PATH = 'null'
    _cache = {}

    @LogCat.log_func
    def __init__(self):
        self._buffer = []
        self._out = b''

    @LogCat.log_func
    def append(self, message: Message) -> None:
        self._buffer.append(message)

    def not_empty(self) -> bool:
        return self._buffer or self._out

    def write(self, socket: socket) -> None:
        if self._out or self._buffer:
            self._out += b''.join([ msg.bytes for msg in self._buffer ])

            out = socket.send(self._out)

            self._out = self._out[out:]
            self._buffer = []

# out_stream.py
