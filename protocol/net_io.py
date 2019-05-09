#!python

import json
import struct

from .message  import Message

class NetIO():
    def __init__(self):
        self._in_buffer = b""

    def recv(self, socket):
        msg = []

        self._in_buffer += socket.recv(1024)

        while len(self._in_buffer) > 4:
            msg_len = struct.unpack(">I", self._in_buffer[:4])[0]

            if len(self._in_buffer) >= (msg_len + 4):
                msg_json = json.loads(
                    str(self._in_buffer[4:msg_len + 4].decode())
                )

                msg.append(
                    Message(msg_json["type"], **msg_json["kwargs"])
                )

                self._in_buffer = self._in_buffer[msg_len+4:]
            else:
                break

        return msg

    def send(self, socket, msg):
        msg_stream = repr(msg).encode()

        socket.sendall(
            struct.pack(">I", len(msg_stream)) + msg_stream
        )

# net_io.py
