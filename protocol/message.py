#!python

import json

class Message():
    def __init__(self, text="noop", **kwargs):
        self.text = text
        self.args = kwargs

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return json.dumps({
            'text': self.text,
            'args': self.args
        })

if __name__ == "__main__":
    msg = Message("sign_in", id="moti", passwd="1234")

    print(msg)
    print(msg.type)
    print(msg.text)
