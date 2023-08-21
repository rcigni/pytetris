from dataclasses import dataclass
from typing import Iterable

from pytetris.logic.tetriminos import Tetrimino, TO, ArcColor


@dataclass(frozen=True)
class LocTetrimino:
    """One tetrimino inside the board."""

    loc: tuple[int, int]
    tetrimino: Tetrimino

    def move(self, orientation: TO):
        return LocTetrimino(
            offset_by(self.loc, orientation),
            self.tetrimino
        )

    def squares(self) -> Iterable[tuple[int, int]]:
        squares = self.tetrimino.squares()
        return [offset(self.loc, square) for square in squares]

    def squares_and_color(self) -> dict[tuple[int, int], ArcColor]:
        squares = self.squares()
        return {sq: self.tetrimino.color for sq in squares}

    def rotate_right(self) -> 'LocTetrimino':
        return LocTetrimino(
            self.loc,
            self.tetrimino.rotate_right()
        )


def offset(loc: tuple[int, int], square: tuple[int, int]) -> tuple[int, int]:
    return loc[0] + square[0], loc[1] + square[1]


OFFSET = {
    TO.UP: (1, 0),
    TO.RIGHT: (0, 1),
    TO.DOWN: (-1, 0),
    TO.LEFT: (0, -1)
}


def offset_by(loc: tuple[int, int], orientation: TO) -> tuple[int, int]:
    return offset(loc, OFFSET[orientation])
