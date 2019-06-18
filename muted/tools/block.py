
from __future__ import annotations

from typing import Tuple

from enum import Enum

class Block(Enum):
    BLOCK = ' '
    CROSSROAD = '┼'
    ROAD_H = ''
    ROAD_V = '┇'
    STREET_H = '╌'
    STREET_V = '┆'
    TRAIL = '.'
    T_RIGHT = '┤'
    T_LEFT = '├'
    T_TOP = '┬'
    T_BOTTOM = '┴'
    CORNER_NE = '╮'
    CORNER_SE = '╯'
    CORNER_NW = '╭'
    CORNER_SW = '╰'
    BANK = '⊡'
    BLACKSMITH = '⚔'
    CLOTHING_STORE = '✄'
    GROCERY_STORE = '⊞'
    HERBAL_STORE = '⚕'
    INN = '∺'
    PAWN_SHOP = '≗'
    RESIDENCE = '⌂'
    TAVERN = '⌅'
    MAILBOX = '✉'
    PINBOARD = '⌗'
    BARREN = '∷'
    FOREST = '⇞'
    GRASSLAND = '⚘'
    HILL = '◬'
    WATER = '≋'
    WATERSIDE = '⌇'
    GUIDEPOST = '⌘'
    HOT_SPRING = '♨'
    GRAVEYARD = '≏'
    POISON = '☠'
    TAI_ZI = '☯'
    WORKSHOP = '⚒'
    STAIR = '⌥'
    MARTIAL_CLUB = '⋌'
    TEA_STALL = '∸'
    BLACK_SUN = '☀'
    WHITE_SUN = '☼'
    CLOUD = '☁'
    UMBRELLA = '☂'
    SNOWY = '☃'
    GATE = '≙'
    TOWN = '⋔'
    TARGET = '⌖'

PASSABLE: Tuple[Block] = (
    Block.BARREN,
    Block.CORNER_NE,
    Block.CORNER_NW,
    Block.CORNER_SE,
    Block.CORNER_SW,
    Block.CROSSROAD,
    Block.STREET_H,
    Block.STREET_V,
    Block.T_BOTTOM,
    Block.T_LEFT,
    Block.T_RIGHT,
    Block.T_TOP,
    Block.GRASSLAND,
    Block.HILL
)

# block.py
