#!python

import json
import socket
import struct
import threading

from protocol.message import Message
from protocol.net_io import NetIO

class Client():
    def __init__(self):
        self._in_buffer = b""
        self._text_handlers = {
           "chat": self._msg_chat,
           "sign_in": self._sign_in,
           "system": self._msg_system,
           "welcome": self._entered
        }

        self._netio = NetIO()
        self._socket = None

    def connect(self, HOST, PORT):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._socket.connect((HOST, PORT))

        threading.Thread(target=self._loop, args=()).start()

    def _sign_in(self):
        user_id = input("使用者名稱：")
        passwd = input("      密碼：")

        self._send_msg(Message(
            "sign_in",
            user_id=user_id,
            passwd=passwd
        ))
 
    def _entered(self):
        threading.Thread(target=self._user_input, args=()).start()

    def _user_input(self):
        while True:
            text = input()

            self._send_msg(
                Message("user", content=text)
            )

    def _loop(self):
        while True:
            received = self._netio.recv(self._socket)

            for msg in received:
                if msg.text in self._text_handlers:
                    self._text_handlers[msg.text](**msg.args)
                else:
                    print(msg)

    def _send_msg(self, msg):
        self._netio.send(self._socket, msg)

    def _msg_chat(self, **kwargs):
        print(f"{kwargs['sender']} 說： {kwargs['content']}")

    def _msg_system(self, **kwargs):
        print(f"{kwargs['sender']} 說： {kwargs['content']}")

if __name__ == "__main__":
    client = Client()

    client.connect("127.0.0.1", 4004)
