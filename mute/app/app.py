
from __future__ import annotations

import curses
import socket

from config.config import CONFIG
from event.event import Event
from event.handler import Handler
from message.out_stream import OutStream
from window_manager.window_manager import WindowManager

from logcat.logcat import LogCat

class App(Handler):
    @LogCat.log_func
    def __init__(self, stdscr):
        super().__init__()

        self._window = stdscr
        self._window_manager = WindowManager()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.on(Event.CURSOR_ON, lambda _: curses.curs_set(True))
        self.on(Event.CURSOR_OFF, lambda _: curses.curs_set(False))
        self.on(Event.WIN_DISPLAY, self._on_win_display)

    @LogCat.log_func
    def add(self, window: Window, modal: bool = False) -> App:
        self._window_manager.add(window, modal)

        return self

    @LogCat.log_func
    def paint(self):
        self._window.border()
        self._window.refresh()

        self._window_manager.on_event(Event(Event.PAINT))

    @LogCat.log_func
    def start(self) -> None:
        self._socket.connect((CONFIG.IP, CONFIG.PORT))
        self._socket.setblocking(0)

        self._loop()

    def _check_input(self) -> None:
        try:
            e = self._window.get_wch()

            if e == 'q':
                Event.trigger(
                    Event(Event.EXIT, self)
                )
            elif e == curses.KEY_MOUSE:
                _, x, y, _, _ = curses.getmouse()

                Event.trigger(
                    Event(
                        Event.CLICK, self._window_manager,
                        x=x, y=y
                    )
                )
            elif type(e) == str:
                LogCat.log(f'keypressed: {e}')
    #        elif e > 0:
                Event.trigger(
                    Event(
                        Event.KEY_PRESSED, self._window_manager.focus,
                        key=e
                    )
                )
            else:
                Event.trigger(
                    Event(
                        e, self._window_manager.focus
                    )
                )

        except curses.error:
            pass

        self._in_stream()

    def _in_stream(self):
        pass

    @LogCat.log_func
    def _loop(self) -> None:
        self.paint()

        while True:
            self._check_input()

            if Event.events():
                events = Event.events().copy()
                Event.empty()

                for e in events:
                    if e.type == Event.EXIT:
                        exit()
                    elif e.target:
                        e.target.on_event(e)
                    else:
                        self.on_event(e)

                self.paint()

            OutStream.instance('').write(self._socket)

    @LogCat.log_func
    def _on_win_display(self, e: Event, uid: str, display: bool) -> None:
        self._window_manager.display(uid, display)

    @property
    def win_manager(self) -> WindowManager:
        return self._window_manager

if __name__ == '__main__':
    main()

# app.py
