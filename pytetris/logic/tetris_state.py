from dataclasses import dataclass
from typing import Iterable

import arcade

from pytetris.logic.loc_tetrimino import LocTetrimino
from pytetris.logic.tetriminos import TO, ArcColor


@dataclass
class TetrisArea:
    size: tuple[int, int]
    _cells_dict: dict[tuple[int, int], arcade.Color]

    def __init__(self, size: tuple[int, int], cells: set[tuple[int, int]] | dict[tuple[int, int] | None, arcade.Color]):
        self.size = size
        if isinstance(cells, set):
            self.cells = cells
        elif isinstance(cells, dict):
            self._cells_dict = cells
        elif cells is None:
            self._cells_dict = dict()
        else:
            raise ValueError("cells must be a set or a dict")

    @property
    def cells(self) -> set[tuple[int, int]]:
        return set(self._cells_dict.keys())

    @cells.setter
    def cells(self, cells: set[tuple[int, int]]):
        self._cells_dict = {cell: arcade.color.GRAY for cell in cells}

    def is_free(self, lp: LocTetrimino) -> bool:
        evaluations = [self._is_free_square(square) for square in (lp.squares())]
        return all(evaluations)

    def _is_free_square(self, loc: tuple[int, int]) -> bool:
        if loc[0] < 0:
            return False
        if loc in self.cells:
            return False
        if 0 <= loc[1] < self.size[1]:
            return True
        else:
            return False

    def will_move(self, p0: LocTetrimino, orientation: TO) -> bool:
        p1 = p0.move(orientation)
        free_piece = self.is_free(p1)
        # if it is a lateral movement, then is WALL
        if (orientation == TO.RIGHT or orientation == TO.LEFT) and free_piece != True:
            return False
        return free_piece

    def add_cells(self, lp: LocTetrimino) -> int:
        self._cells_dict.update(lp.squares_and_color())
        completed_line = self.has_completed_line()
        if len(completed_line) > 0:
            self.remove_cells_by_line(completed_line)
            self.apply_gravity(completed_line)
        return len(completed_line)

    def has_completed_line(self) -> set[int]:
        completed = set()
        for row in range(self.size[0]):
            if all((row, col) in self.cells for col in range(self.size[1])):
                completed.add(row)
        return completed

    def remove_cells_by_line(self, lines: Iterable[int]):
        for cell in list(self._cells_dict.keys()):
            if cell[0] in lines:
                del self._cells_dict[cell]
        return self.cells

    def apply_gravity(self, removed_lines: Iterable[int]) -> None:
        cells = dict()
        for cell in self._cells_dict.keys():
            dec = 0
            for line in removed_lines:
                if cell[0] > line:
                    dec += 1
            cells[(cell[0] - dec, cell[1])] = self._cells_dict[cell]
        self._cells_dict = cells

    def enter_position(self):
        return self.size[0] - 1, self.size[1] // 2

    def cells_and_colors(self) -> dict[tuple[int, int], ArcColor]:
        return self._cells_dict
