#!python

import json
import selectors
import struct

from protocol.message import Message

class Guest():
    def __init__(self):
        self._in_buffer = b""
        self._msg_out = []

        self.user = 'guest'
        self.msg_in = []

    def on_socket(self, socket, mask):
        if mask & selectors.EVENT_READ:
            self._in_buffer += socket.recv(1024)

            while len(self._in_buffer) > 4:
                msg_len = struct.unpack(">I", self._in_buffer[:4])[0]

                if len(self._in_buffer) >= (msg_len + 4):
                    msg_json = json.loads(
                        str(self._in_buffer[4:msg_len + 4].decode())
                    )

                    self.msg_in.append(
                        Message(msg_json["text"], **msg_json["args"])
                    )

                    self._in_buffer = self._in_buffer[msg_len+4:]
                else:
                    break

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

    def handle_msg(self):
        for msg in self.msg_in:
            self._text_handlers[msg.text](**msg.args)

        self.msg_in = []
