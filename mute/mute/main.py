#!/usr/bin/python3

import curses

from const.color import Color
from mute.mute import Mute

from logcat.logcat import LogCat

@LogCat.log_func
def curses_init():
    curses.curs_set(False)
    curses.mousemask(1)

    curses.use_default_colors()

    curses.init_pair(
        Color.BUTTON, Color.FOREGROUND, Color.BUTTON_BACKGROUND
    )

    curses.init_pair(
        Color.INPUT_FIELD, Color.FOREGROUND, Color.FIELD_BACKGROUND
    )

    curses.init_pair(
        Color.SCROLL_BAR, Color.FOREGROUND, Color.SCROLL_BAR_BACKGROUND
    )

    curses.init_pair(
        Color.TEXT, Color.FOREGROUND, Color.BACKGROUND
    )

    Color.BUTTON = curses.color_pair(Color.BUTTON)
    Color.INPUT_FIELD = curses.color_pair(Color.INPUT_FIELD)
    Color.SCROLL_BAR = curses.color_pair(Color.SCROLL_BAR)
    Color.TEXT = curses.color_pair(Color.TEXT)

@LogCat.log_func
def main(stdscr):
    curses_init()

    stdscr.nodelay(True)

    a = Mute(stdscr)
    a.start()

if __name__ == '__main__':
    curses.wrapper(main)

# main.py
