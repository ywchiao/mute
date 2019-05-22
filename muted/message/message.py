
from __future__ import annotations

import json
import struct

from logcat.logcat import LogCat

class Message:
    CHAT = 'chat'
    SIGN_IN = 'sign_in'
    SYSTEM = 'system'
    TEXT = 'text'
    WELCOME = 'welcome'

    def __init__(self, type: str, **kwargs: dict):
        self._type = type
        self._kwargs = kwargs

        stream = repr(self).encode()
        self._bytes = struct.pack('>I', len(stream)) + stream

    @property
    def bytes(self) -> bytes:
        return self._bytes

    @property
    def type(self) -> str:
        return self._type

    @property
    def kwargs(self):
        return self._kwargs

    def __repr__(self) -> str:
        return json.dumps({
            'type': self._type,
            'kwargs': self._kwargs
        })

if __name__ == '__main__':
    msg = Message('sign_in', id='moti', passwd='1234')

    print(msg)
    print(msg.type)

# message.py
