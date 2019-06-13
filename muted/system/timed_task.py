
from __future__ import annotations

from typing import Any
from typing import NamedTuple

import time

from logcat.logcat import LogCat

class Task(NamedTuple):
    content: Any
    schedule: float
    delay: float

class TimedTask:
    _instance: TimedTask = None

    @LogCat.log_func
    def __init__(self):
        self._queue: List[Task] = []

    @classmethod
    def instance(cls) -> TimedTask:
        if not cls._instance:
            cls._instance = TimedTask()

        return cls._instance

    @classmethod
    def schedule(cls, o, delay: int) -> None:
        d = delay * 1000000000

        cls.instance()._schedule(Task(o, d + time.time_ns(), d))

    @classmethod
    def update(cls) -> None:
        cls.instance()._update()

    def _schedule(self, task: Task) -> None:
        self._queue.append(task)

    def _update(self) -> None:
        self._queue = [
            task if time.time_ns() < task.schedule else
            Task(task.content, task.schedule + task.delay, task.delay)
            if not task.content.update() else None
            for task in self._queue if task
        ]

# timed_task.py
