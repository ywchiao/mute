
import selectors
import socket

from guest.guest import Guest
from protocol.message import Message

class Serverlet:
    def __init__(self):
        self._guests = []
        self._multiplexer = selectors.DefaultSelector()
        self._text_handlers = {
            "sign_in": self._sign_in,
            "user": self._msg_chat
        }

    def on_socket(self, server_socket, mask):
        connection, address = server_socket.accept()  # Should be ready to read
        print(f"Connected by: {address}")

        connection.setblocking(False)

        mask = selectors.EVENT_READ | selectors.EVENT_WRITE

        guest = Guest()

        self._multiplexer.register(connection, mask, guest)

        self._guests.append(guest)

        guest.send_msg(Message(
            "system",
            sender="MUTE",
            content=f"歡迎來到 MUTE: Multi-User Texting Environment"
        ))

        guest.send_msg(Message(
            "sign_in"
        ))

    def start(self, HOST, PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
            serverSocket.bind((HOST, PORT))
            serverSocket.setblocking(False)
            serverSocket.listen()

            self._multiplexer.register(
                serverSocket, selectors.EVENT_READ, self
            )

            print(f"MUTE server start listening at {HOST}:{PORT}")

            while True:
                events = self._multiplexer.select(timeout=None)

                for io, mask in events:
                    io.data.on_socket(io.fileobj, mask)

                for guest in self._guests:
                    for msg in guest.msg_in:
                        print(f"{guest.user}: {msg}")

                        if msg.text in self._text_handlers:
                            self._text_handlers[msg.text](guest, **msg.args)

                    guest.msg_in = []

    def _msg_chat(self, sender, **kwargs):
        for guest in self._guests:
            guest.send_msg(Message(
                "chat",
                sender=sender.user,
                content=kwargs["content"]
            ))

    def _sign_in(self, guest, **kwargs):
        print(f"id: {kwargs['user_id']} passwd {kwargs['passwd']}")
        guest.set_user(kwargs["user_id"])

        guest.send_msg(Message("welcome"))

if __name__ == "__main__":
    serverlet = Serverlet()

    serverlet.start("127.0.0.1", 4004)
