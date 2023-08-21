import dataclasses
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum, auto

import arcade.color as clr

ArcColor = tuple[int, int, int]

class TT(Enum):
    """ Piece Types """
    STICK = auto()
    L1 = auto()
    L2 = auto()
    S1 = auto()
    S2 = auto()
    SQUARE = auto()
    T = auto()


TTs: list[TT] = list(TT)

COLORs = {
    TT.L1: clr.RED,
    TT.L2: clr.ORANGE,
    TT.S1: clr.BLUE,
    TT.S2: clr.AERO_BLUE,
    TT.T:  clr.GREEN,
    TT.SQUARE: clr.PURPLE,
    TT.STICK: clr.YELLOW
}

class TO(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


ROTATION_RIGHT = {
    TO.UP: TO.RIGHT,
    TO.RIGHT: TO.DOWN,
    TO.DOWN: TO.LEFT,
    TO.LEFT: TO.UP
}

@dataclass(frozen=True)
class Tetrimino:

    orientation: TO
    color: clr
    shape: dict[TO, list[tuple[int, int]]]

    def squares(self) -> Iterable[tuple[int, int]]:
        return self.shape[self.orientation]

    def rotate_right(self):
        return dataclasses.replace(self, orientation=(self.get_rotate_right()))

    def get_rotate_right(self):
        return ROTATION_RIGHT[self.orientation]


STICK_SHAPES = {
    TO.UP: [(0, 0), (0, 1), (0, 2), (0, 3)],
    TO.RIGHT: [(0, 0), (1, 0), (2, 0), (3, 0)],
    TO.LEFT: [(0, 0), (1, 0), (2, 0), (3, 0)],
    TO.DOWN: [(0, 0), (0, 1), (0, 2), (0, 3)],
}

L1_SHAPES = {
    TO.DOWN: [(0, 0), (0, 1), (0, 2), (1, 0)],
    TO.UP: [(0, 0), (1, 1), (2, 1), (0, 1)],
    TO.LEFT: [(0, 0), (1, 0), (2, 0), (2, 1)],
    TO.RIGHT: [(0, 2), (1, 2), (1, 1), (1, 0)]
}

L2_SHAPES = {
    TO.DOWN: [(0, 2), (1, 2), (0, 1), (0, 0)],
    TO.UP: [(1, 2), (1, 1), (1, 0), (0, 0)],
    TO.LEFT: [(0, 1), (1, 1), (2, 1), (2, 0)],
    TO.RIGHT: [(0, 0), (1, 0), (2, 0), (0, 1)]
}

T_SHAPES = {
    TO.UP: [(0, 1), (1, 1), (2, 1), (1, 0)],
    TO.LEFT: [(1, 2), (1, 1), (1, 0), (2, 1)],
    TO.DOWN: [(0, 1), (1, 1), (2, 1), (1, 2)],
    TO.RIGHT: [(1, 2), (1, 1), (1, 0), (0, 1)]
}

S1_SHAPES = {
    TO.UP: [(1, 2), (1, 1), (0, 1), (0, 0)],
    TO.DOWN: [(1, 2), (1, 1), (0, 1), (0, 0)],
    TO.LEFT: [(0, 1), (1, 1), (1, 0), (2, 0)],
    TO.RIGHT: [(0, 1), (1, 1), (1, 0), (2, 0)]
}

S2_SHAPES = {
    TO.UP: [(0, 2), (0, 1), (1, 1), (1, 0)],
    TO.DOWN: [(0, 2), (0, 1), (1, 1), (1, 0)],
    TO.LEFT: [(1, 1), (2, 1), (1, 0), (0, 0)],
    TO.RIGHT: [(1, 1), (2, 1), (1, 0), (0, 0)]
}

SQUARE_SHAPES = {
    TO.UP: [(0, 0), (0, 1), (1, 1), (1, 0)]
}
SQUARE_SHAPES[TO.DOWN] = SQUARE_SHAPES[TO.UP]
SQUARE_SHAPES[TO.RIGHT] = SQUARE_SHAPES[TO.UP]
SQUARE_SHAPES[TO.LEFT] = SQUARE_SHAPES[TO.UP]

class SquareTetrimino(Tetrimino):

    def squares(self):
        return SQUARE_SHAPES[self.orientation]

def new_tetrimino_by_type(piece_type: TT, orientation: TO = TO.UP) -> Tetrimino:
    color = COLORs[piece_type]
    match piece_type:
        case TT.STICK:
            return Tetrimino(orientation, color, STICK_SHAPES)
        case TT.L1:
            return Tetrimino(orientation, color, L1_SHAPES)
        case TT.L2:
            return Tetrimino(orientation, color, L2_SHAPES)
        case TT.T:
            return Tetrimino(orientation, color, T_SHAPES)
        case TT.S1:
            return Tetrimino(orientation, color, S1_SHAPES)
        case TT.S2:
            return Tetrimino(orientation, color, S2_SHAPES)
        case TT.SQUARE:
            return Tetrimino(orientation, color, SQUARE_SHAPES)
        case _:
            raise ValueError(f"Invalid piece type ${piece_type}")