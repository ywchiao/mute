
import json
import selectors
import struct

from protocol.message import Message
from protocol.net_io import NetIO

class Guest():
    def __init__(self):
        self._in_buffer = b""
        self._msg_out = []
        self._netio = NetIO()

        self.user = 'guest'
        self.msg_in = []

    def on_socket(self, socket, mask):
        if mask & selectors.EVENT_READ:
            self.msg_in = self._netio.recv(socket)

        if mask & selectors.EVENT_WRITE:
            data = []

            for msg in self._msg_out:
                msg_stream = repr(msg).encode()

                data.append(
                    struct.pack(">I", len(msg_stream)) + msg_stream
                )

            socket.sendall(b''.join(data))

            self._msg_out = []

    def set_user(self, user):
        self.user = user

    def send_msg(self, msg):
        self._msg_out.append(msg)

# guest.py
