
from __future__ import annotations

import selectors
import socket

from config.config import CONFIG
from entity.entity import Entity
from event.event import Event
from message.message import Message
from message.in_stream import InStream
from message.out_stream import OutStream
from system.servant import Servant

from logcat.logcat import LogCat

class Muted:
    @LogCat.log_func
    def __init__(self):
        super().__init__()

        self._multiplexer = selectors.DefaultSelector()

    @LogCat.log_func
    def start(self, HOST, PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.setblocking(False)
            server_socket.listen()

            self._multiplexer.register(
                server_socket, selectors.EVENT_READ, ''
            )

            print(f'MUTE server start listening at {HOST}:{PORT}')

            self._loop()

    def _loop(self) -> None:
        while True:
            self._on_net_io()

            if Event.events():
                events = Event.events().copy()
                Event.empty()

                for e in events:
                    if e.target:
                        e.target.on_event(e)
                    else:
                        self.on_event(e)

    def _on_read(self, socket: socket, entity: str) -> None:
        msg_buffer = InStream.instance(entity).read(socket)

        for msg in msg_buffer:
            Event.trigger(
                Event(
                    msg.type, Servant.instance(),
                    entity=entity,
                    **msg.kwargs
                )
            )

    def _on_net_io(self) -> None:
        events = self._multiplexer.select(timeout=None)

        for io, mask in events:
            if mask & selectors.EVENT_READ:
                if io.data:
                    self._on_read(io.fileobj, io.data)
                else:
                    self._on_new_connection(io.fileobj)

            if mask & selectors.EVENT_WRITE:
                OutStream.instance(io.data).write(io.fileobj)

    def _on_new_connection(self, socket: socket) -> None:
        connection, address = socket.accept()  # Should be ready to read
        print(f'Connected by: {address}')

        connection.setblocking(False)

        mask = selectors.EVENT_READ | selectors.EVENT_WRITE

        entity = Entity.eid()

        self._multiplexer.register(connection, mask, entity)

        Event.trigger(
            Event(
                Event.RECEPTION, Servant.instance(),
                entity=entity
            )
        )

if __name__ == '__main__':
    muted = Muted()

    muted.start(CONFIG.IP, CONFIG.PORT)

# muted.py
