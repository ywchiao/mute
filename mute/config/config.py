
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
            path = Path(f'.mute/mute.json')

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
                           'log': './.mute/log'
                       },
                       'log': {
                           'config': 'config.json',
                           'file': 'mute.log'
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

CONFIG = Config.instance()

# config.py
