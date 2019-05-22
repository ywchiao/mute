
from __future__ import annotations

from typing import List
from typing import Mapping

import json
import socket
import struct

from facet.facet import Facet
from message.message import Message

from logcat.logcat import LogCat

class InStream(Facet):
    DATA_PATH = 'null'
    _cache: Mapping[str, InStream] = {}

    @LogCat.log_func
    def __init__(self):
        self._in = b''

    def read(self, socket: socket) -> List[Message]:
        msg_buffer = []

        try:
            self._in += socket.recv(4096)
        except:
            pass

        while len(self._in) > 4:
            msg_len = struct.unpack('>I', self._in[:4])[0]

            if len(self._in) >= (msg_len + 4):
                msg = json.loads(
                    str(self._in[4:msg_len + 4].decode())
                )

                msg_buffer.append(
                    Message(msg['type'], **msg['kwargs'])
                )

                self._in = self._in[msg_len+4:]
            else:
                break

        return msg_buffer

# in_stream.py
