
from __future__ import annotations

import selectors
import socket

from config.config import CONFIG
from entity.entity import Entity
from event.event import Event
from message.in_stream import InStream
from message.out_stream import OutStream
from system.servant import Servant

from logcat.logcat import LogCat

class NetIO:
    @LogCat.log_func
    def __init__(self, socket: socket):
        self._servant = Servant.instance()

        socket.bind((CONFIG.IP, CONFIG.PORT))
        socket.setblocking(False)

        self._multiplexer = selectors.DefaultSelector()

        self._multiplexer.register(
            socket, selectors.EVENT_READ, ''
        )

        socket.listen()

        print(f'MUTED server start listening at {CONFIG.IP}:{CONFIG.PORT}')

    def check(self) -> None:
        events = self._multiplexer.select(timeout=None)

        for io, mask in events:
            if mask & selectors.EVENT_READ:
                if io.data:
                    self._read(io.data, io.fileobj)
                else:
                    self._new_connection(io.fileobj)

            if mask & selectors.EVENT_WRITE:
                OutStream.instance(io.data).write(io.fileobj)

    def _new_connection(self, socket: socket) -> None:
        connection, address = socket.accept()  # Should be ready to read
        print(f'Connected by: {address}')

        connection.setblocking(False)

        mask = selectors.EVENT_READ | selectors.EVENT_WRITE

        entity = Entity.eid()

        self._multiplexer.register(connection, mask, entity)

        Event.trigger(
            Event(
                Event.RECEPTION, self._servant,
                entity=entity
            )
        )

    def _read(self, entity: str, socket: socket) -> None:
        for msg in InStream.instance(entity).read(socket):
            Event.trigger(
                Event(
                    msg.type, self._servant,
                    entity=entity,
                    **msg.kwargs
                )
            )

# net_io.py
