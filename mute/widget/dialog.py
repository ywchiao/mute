
from __future__ import annotations

from event.event import Event
from widget.button import Button
from widget.window import Window

from logcat.logcat import LogCat

class Dialog(Window):
    @LogCat.log_func
    def __init__(self, x: int, y:int, width: int, height: int):
        super().__init__(x, y, width, height)

        btn_x = (width - 14) // 2
        self._caption = None
        self._modal = True

        self._btn_ok = Button(btn_x, height - 2, '確定')
        self._btn_cancel = Button(btn_x + 8, height - 2, '取消')

        self._btn_ok.on(Event.CLICK, self._on_click_ok)
        self._btn_cancel.on(Event.CLICK, self._on_click_cancel)

        self.add(self._btn_ok)
        self.add(self._btn_cancel)

        self._focus = self._btn_ok

    def _on_click_cancel(self, e: Event, x: int, y: int) -> None:
        Event.trigger(
            Event(
                Event.WIN_DISPLAY, None, uid=self.uid, display=False
            )
        )

        Event.trigger(
            Event(
                Event.DIALOG_CANCEL, self
            )
        )

    def _on_click_ok(self, e: Event, x: int, y: int) -> None:
        Event.trigger(
            Event(
                Event.WIN_DISPLAY, None, uid=self.uid, display=False
            )
        )

        Event.trigger(
            Event(
                Event.DIALOG_OK, self
            )
        )

    @property
    def button_ok(self):
        return self._btn_ok

# dialog.py
