#!python

import json

class Message:
    CHAT = "chat"
    SIGN_IN = "sign_in"
    SYSTEM = "system"
    WELCOME = "welcome"

    def __init__(self, type_="noop", **kwargs):
        self._type = type_
        self._kwargs = kwargs

    @property
    def type(self):
        return self._type

    @property
    def kwargs(self):
        return self._kwargs

    def __repr__(self):
        return json.dumps({
            'type': self._type,
            'kwargs': self._kwargs
        })

if __name__ == "__main__":
    msg = Message("sign_in", id="moti", passwd="1234")

    print(msg)
    print(msg.type)
    print(msg.text)

# message.py
