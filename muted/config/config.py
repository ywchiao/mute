
from __future__ import annotations

import json

from pathlib import Path

class Config:
    _instance: Config = None

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    @classmethod
    def instance(cls) -> Config:
        if not cls._instance:
            path = Path(f'.muted/muted.json')

            if path.is_file():
                with path.open() as fin:
                    cls._instance = Config(**json.load(fin))
            else:
                cls._instance = Config(
                   **{
                       'socket': {
                           'ip': '127.0.0.1',
                           'port': 4004
                       },
                       'root': {
                           'data': './.muted/data',
                           'log': './.muted/log'
                       },
                       'log': {
                           'config': 'config.json',
                           'file': 'muted.log'
                       },
                       'data': {
                           'brief': 'brief',
                           'desc': 'desc',
                           'exit': 'exit',
                           'genus': 'genus',
                           'name': 'name',
                           'role': 'role',
                           'room': 'room'
                       }
                   }
                )

        return cls._instance

    @property
    def IP(self) -> str:
        return self._kwargs['socket']['ip']

    @property
    def PORT(self) -> int:
        return self._kwargs['socket']['port']

    @property
    def LOG_CONFIG(self) -> str:
        return (
            f'{self._kwargs["root"]["log"]}/'
            f'{self._kwargs["log"]["config"]}'
        )

    @property
    def LOG_FILE(self) -> str:
        return (
            f'{self._kwargs["root"]["log"]}/'
            f'{self._kwargs["log"]["file"]}'
        )

    @property
    def BAGGAGE(self) -> str:
        return (
            f'{self._kwargs["root"]["data"]}/'
            f'{self._kwargs["data"]["baggage"]}'
        )

    @property
    def BRIEF(self) -> str:
        return (
            f'{self._kwargs["root"]["data"]}/'
            f'{self._kwargs["data"]["brief"]}'
        )

    @property
    def DESCRIPTION(self) -> str:
        return (
            f'{self._kwargs["root"]["data"]}/'
            f'{self._kwargs["data"]["desc"]}'
        )

    @property
    def EXIT(self) -> str:
        return (
            f'{self._kwargs["root"]["data"]}/'
            f'{self._kwargs["data"]["exit"]}'
        )

    @property
    def GENUS(self) -> str:
        return (
            f'{self._kwargs["root"]["data"]}/'
            f'{self._kwargs["data"]["genus"]}'
        )

    @property
    def LEVEL(self) -> str:
        return (
            f'{self._kwargs["root"]["data"]}/'
            f'{self._kwargs["data"]["level"]}'
        )

    @property
    def NAME(self) -> str:
        return (
            f'{self._kwargs["root"]["data"]}/'
            f'{self._kwargs["data"]["name"]}'
        )

    @property
    def NPC(self) -> str:
        return (
            f'{self._kwargs["root"]["data"]}/'
            f'{self._kwargs["data"]["npc"]}'
        )

    @property
    def PASSER(self) -> str:
        return (
            f'{self._kwargs["root"]["data"]}/'
            f'{self._kwargs["data"]["passer"]}'
        )

    @property
    def ROLE(self) -> str:
        return (
            f'{self._kwargs["root"]["data"]}/'
            f'{self._kwargs["data"]["role"]}'
        )

    @property
    def ROOM(self) -> str:
        return (
            f'{self._kwargs["root"]["data"]}/'
            f'{self._kwargs["data"]["room"]}'
        )

CONFIG = Config.instance()

# config.py
