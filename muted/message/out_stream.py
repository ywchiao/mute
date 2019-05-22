
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

    def write(self, socket: socket) -> None:
        self._out += b''.join([ msg.bytes for msg in self._buffer ])

        out = socket.send(self._out)

        self._out = self._out[out:]
        self._buffer = []

    def append(self, message: Message) -> None:
        self._buffer.append(message)

# out_stream.py
