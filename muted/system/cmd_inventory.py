
from __future__ import annotations

from typing import List
from typing import Type

from component.bag import Bag

from event.event import Event
from message.message import Message
from system.channel import Channel

from logcat.logcat import LogCat

class CmdInventory:
    @LogCat.log_func
    def __init__(self, servant: Type[Handler]):
        servant.on(Event.CMD_INVENTORY, self._on_cmd_inventory)
        servant.on(Event.CMD_ABBR_INVENTORY, self._on_cmd_inventory)

    @LogCat.log_func
    def _on_cmd_inventory(
        self, e: Event, entity: str = '', args: List[str] = []
    ) -> None:
        if not Bag.instance(entity):
            text = f'  你身上沒有東西。'
        else:
            text = f'  你身上有：'

#        for text in inventory:
#            Channel.to_role(entity, Message.TEXT, text)
        Channel.to_role(entity, Message.TEXT, text)

# cmd_inventory.py
