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
        self._handlers = {
           Message.CHAT: self._on_msg_chat,
           Message.SIGN_IN: self._on_sign_in,
           Message.SYSTEM: self._on_msg_system,
           Message.WELCOME: self._on_entered
        }

        self._netio = NetIO()
        self._socket = None
        self._user = "guest"

    def connect(self, HOST, PORT):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._socket.connect((HOST, PORT))

        threading.Thread(target=self._loop, args=()).start()

    def _loop(self):
        while True:
            received = self._netio.recv(self._socket)

            for msg in received:
                if msg.type in self._handlers:
                    self._handlers[msg.type](**msg.kwargs)
                else:
                    print(msg)

    def _on_entered(self, **kwargs):
        self._user = kwargs["guest"]

        threading.Thread(target=self._user_input, args=()).start()

    def _on_msg_chat(self, **kwargs):
        print(f"{kwargs['who']} 說： {kwargs['text']}")

    def _on_msg_system(self, **kwargs):
        print(f"{kwargs['who']} 說： {kwargs['text']}")

    def _on_sign_in(self):
        user_id = input("使用者名稱：")
        passwd = input("      密碼：")

        self._send_msg(Message(
            Message.SIGN_IN,
            user_id=user_id,
            passwd=passwd
        ))
 
    def _send_msg(self, msg):
        self._netio.send(self._socket, msg)

    def _user_input(self):
        while True:
            text = input()

            self._send_msg(
                Message(Message.CHAT, who=self._user, text=text)
            )

if __name__ == "__main__":
    client = Client()

    client.connect("127.0.0.1", 4004)

# client.py
