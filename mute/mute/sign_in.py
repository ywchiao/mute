
from __future__ import annotations

from event.event import Event
from widget.dialog import Dialog
from widget.field import Field
from widget.label import Label

from logcat.logcat import LogCat

class SignIn(Dialog):
    @LogCat.log_func
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)

        self._field_id = Field(8, 2, 12)
        self._field_id.on(Event.LINEFEED, self._on_linefeed_id)

        self._field_passwd = Field(8, 4, 12)
        self._field_passwd.on(Event.LINEFEED, self._on_linefeed_passwd)

        self.add(Label(2, 2, 'ID'))
        self.add(self._field_id)
        self.add(Label(2, 4, '密碼'))
        self.add(self._field_passwd)

        self.set_caption('登 入')

    @LogCat.log_func
    def _on_linefeed_id(self, e: Event) -> None:
        Event.trigger(
            Event(
                Event.CLICK, self,
                x=self.left + self._field_passwd.left,
                y=self.top + self._field_passwd.top
            )
        )

        return self._field_id.value

    @LogCat.log_func
    def _on_linefeed_passwd(self, e: Event) -> None:
        Event.trigger(
            Event(Event.FOCUS_OUT, self)
        )

        Event.trigger(
            Event(Event.CLICK, self.button_ok, x=0, y=0)
        )

        return self._field_passwd.value

    @property
    def user_id(self):
        return self._field_id.value

    @property
    def passwd(self):
        return self._field_passwd.value

# sign_in.py
