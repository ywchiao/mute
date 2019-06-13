
from __future__ import annotations

from typing import List
from typing import Type

from component.link import Link
from component.stats import Stats

from event.event import Event
from message.message import Message
from system.attack import Attack
from system.channel import Channel
from system.timed_task import TimedTask

from logcat.logcat import LogCat

class CmdKill:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        self._servant = servant

        servant.on(Event.CMD_KILL, self._on_cmd_kill)
        servant.on(Event.CMD_ABBR_KILL, self._on_cmd_kill)

    @LogCat.log_func
    def _on_cmd_kill(
        self, e: Event, entity: str = '', args: List[str] = []
    ) -> None:
        role = Stats.text('binding', entity)
        room = Stats.text('at_room', role)

        if not args:
            text = f'  你想要殺誰？'
        else:
            target = self._get_target(room, args[0])

            if not target:
                text = f'  這裡沒有這個人。'
            else:
                name = Stats.text('name', target.role)
                text = f'  你大喝一聲：「{name}納命來。」就朝{name}發起攻擊。'

                attacker = Link(entity, role)

                TimedTask.schedule(
                    Attack(attacker, target), Attack.TICK_NORMAL
                )

                TimedTask.schedule(
                    Attack(target, attacker), Attack.TICK_NORMAL
                )

        Channel.to_role(entity, Message.TEXT, text)

    def _get_target(self, room: str, tag: str) -> Link:
        target = None

        for guest in Stats.list_items('guest', room):
            if tag == Stats.text('tag', guest.role):
                target = guest
                break
        else:
            for passer in Stats.list_items('passer', room):
                if tag == Stats.text('tag', passer):
                    target = Link(None, passer)
                    break

        return target

# cmd_kill.py
