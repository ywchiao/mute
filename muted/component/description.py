
from __future__ import annotations

from typing import List

from config.config import CONFIG
from facet.facet import Facet

from logcat.logcat import LogCat

class Description(Facet):
    DATA_PATH = CONFIG.DESCRIPTION
    _cache = {}

    @LogCat.log_func
    def __init__(
        self,
        desc: List[str] = [
            f'Muter 還沒有為這個 [物件] 建立任何描述；或者，更糟的',
            f'是，相關的內容已丟失或遺落在未知的時空。',
            f'如果可以，請你協助通知的相關人士，的未來掌握在看',
            f'到這段訊息的人手上。'
        ]
    ):
        self._desc = desc

    @property
    def text(self) -> List[str]:
        return self._desc

# description.py
