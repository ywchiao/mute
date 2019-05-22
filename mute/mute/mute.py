
from app.app import App
from event.event import Event
from config.config import CONFIG
from message.message import Message
from message.in_stream import InStream
from message.out_stream import OutStream
from mute.sign_in import SignIn
from widget.field import Field
from widget.text_box import TextBox
from widget.window import Window

from logcat.logcat import LogCat

class Mute(App):
    @LogCat.log_func
    def __init__(self, stdscr):
        super().__init__(stdscr)

        self._user = 'guest'

        self._text_box = TextBox(1, 1, 58, 19)

        self._content = Window(
            0, 0, 60, 21, 'MUTE: Multi-User Texting Environment'
        )
        self._content.add(self._text_box)

        self._input_frame = Window(0, 21, 60, 3)

        self._aside = Window(60, 0, 20, 24)

        self._input_field = Field(1, 1, 58)
        self._input_field.on(Event.LINEFEED, self._on_msg_entered)

        self._input_frame.add(self._input_field)

        self.add(self._content)
        self.add(self._input_frame)
        self.add(self._aside)

        self._sign_in = self._sign_in()

        self.add(self._sign_in, True)

        self.on(Message.CHAT, self._on_msg_chat)
        self.on(Message.SYSTEM, self._on_msg_system)
        self.on(Message.TEXT, self._on_msg_text)
        self.on(Message.SIGN_IN, self._on_msg_sign_in)

    def _in_stream(self) -> None:
        for msg in InStream.instance('').read(self._socket):
            Event.trigger(
                Event(msg.type, self, **msg.kwargs)
            )

    @LogCat.log_func
    def _on_dlg_cancel(self, e: Event) -> None:
        Event.trigger(
            Event(Event.EXIT, self)
        )

    @LogCat.log_func
    def _on_dlg_ok(self, e: Event) -> None:
        self._user = e.target.user_id

        OutStream.instance('').append(
            Message(
                type=Event.SIGN_IN,
                user_id=e.target.user_id,
                passwd=e.target.passwd
            )
        )

    @LogCat.log_func
    def _on_msg_chat(self, e: Event, who: str, text: str) -> None:
        self._text_box.add_text(f'{who} 說： {text}')

    @LogCat.log_func
    def _on_msg_entered(self, text: str) -> str:
        OutStream.instance('').append(
            Message(
                type=Message.TEXT,
                who=self._user,
                text=text
            )
        )

        return ''

    @LogCat.log_func
    def _on_msg_system(self, e: Event, who: str, text: str) -> None:
        self._text_box.add_text(f'{who} 說： {text}')

    @LogCat.log_func
    def _on_msg_text(self, e: Event, who: str, text: str) -> None:
        self._text_box.add_text(f'  {text}')

    @LogCat.log_func
    def _on_msg_sign_in(self, e: Event, who: str) -> None:
        Event.trigger(
            Event(
                Event.WIN_DISPLAY, self,
                uid=self._sign_in.uid,
                display=True
            )
        )

    @LogCat.log_func
    def _sign_in(self):
        sign_in = SignIn(19, 5, 22, 9)

        sign_in.on(Event.DIALOG_OK, self._on_dlg_ok)
        sign_in.on(Event.DIALOG_CANCEL, self._on_dlg_cancel)

        return sign_in

# mute.py
