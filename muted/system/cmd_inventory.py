
from __future__ import annotations

from typing import List
from typing import Type

from component.baggage import Baggage

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
        items = [
            item
            for bag in Baggage.instance(entity).items
            for item in Baggage.instance(bag).items
        ]

        if not items:
            inventory = [ f'  你身上沒有東西。' ]
        else:
            inventory = [ f'你身上帶著有：' ]

            for item in items:
                inventory.append(
                    f'  {Name.instance(item).text}'
                )

        for text in inventory:
            Channel.to_role(entity, Message.TEXT, text)

# cmd_inventory.py
