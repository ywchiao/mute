
from __future__ import annotations

from config.config import CONFIG
from facet.facet import Facet

from logcat.logcat import LogCat

class NPC(Facet):
    DATA_PATH = CONFIG.NPC
    _cache = {}

    @LogCat.log_func
    def __init__(
        self,
        brief: str = '一位一臉茫然，不知道自己為何在這兒出現的人。',
        description: list = [
            '他站在那兒，一臉的茫然。他不認識這兒，他壓根兒不知他',
            '什麼會在這兒出現。他低頭看看身上的衣服，他沒見有人這',
            '樣穿過，至少在他記憶裡沒有。',
            '我是誰？我為什麼在這裡？我要作什麼？他苦惱的想著。'
        ],
        name: str = '臨時演員',
    ):
        pass

# npc.py
