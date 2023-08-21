import pytest

from pytetris.logic.loc_tetrimino import LocTetrimino
from pytetris.logic.tetriminos import TO, new_tetrimino_by_type, TT
from pytetris.logic.tetris_state import TetrisArea

BOARD_SIZE = (20, 10)

@pytest.mark.parametrize("cells,position,expected", [
    ({}, (0, 0), True),
    ({(0, 0)}, (0, 0), False),
    ({}, (-1, 0), False),
    ({}, (0, 9), True),
    ({}, (0, -1), False),
    ({}, (0, 10), False),
    ({}, (0, 20), False),
    ({(8, 7)}, (8, 8), True),
])
def test_tetris_is_free_square(cells, position, expected):
    state = TetrisArea(size=BOARD_SIZE, cells=cells)
    assert state._is_free_square(position) is expected

@pytest.mark.parametrize("cells,position,expected", [
    ({}, (0, 0), True),
    ({(0, 0)}, (0, 0), False),
    ({(0, 2), (1, 2), (2, 2), (2, 0), (2, 1)}, (0, 0), True),
    ({}, (8, 0), True),
    ({}, (10, 8), True),
    ({}, (10, 10), False),
    ({}, (10, 20), False),
])
def test_tetris_is_free_piece(cells, position, expected):
    state = TetrisArea(size=BOARD_SIZE, cells=cells)
    piece = new_tetrimino_by_type(TT.SQUARE)
    assert state.is_free(LocTetrimino(position, piece)) is expected

@pytest.mark.parametrize("cells,position,expected", [
    (set(), (5, 7), True),
])
def test_tetris_is_free_piece_l1(cells, position, expected):
    state = TetrisArea(size=BOARD_SIZE, cells=cells)
    piece = new_tetrimino_by_type(TT.L1)
    assert state.is_free(LocTetrimino(position, piece)) is expected

@pytest.mark.parametrize("cells,p0, orientation, expected", [
    (set(), (0, 0), TO.UP, True),
    (set(), (5, 8), TO.RIGHT, False),
    (set(), (8, 8), TO.DOWN, True),
    ({(8, 7)}, (8, 8), TO.LEFT, False),
    (set(), (8, 8), TO.DOWN, True),
])
def test_tetris_will_transit(cells, p0, orientation, expected):
    piece = new_tetrimino_by_type(TT.SQUARE)
    state = TetrisArea(size=BOARD_SIZE, cells=cells)
    assert state.will_move(LocTetrimino(p0, piece), orientation) is expected

@pytest.mark.parametrize("cells,expected", [
    ({}, set()),
    ({(2, 0), (2, 1), (2, 2)}, set()),
    ({(2, 0), (2, 1), (2, 2), (2, 3)}, {2}),
    ({
         (2, 0), (2, 1), (2, 2), (2, 3),
         (3, 0),
         (4, 0), (4, 1), (4, 2), (4, 3)
     }, {2, 4})
])
def test_is_line_full(cells, expected):
    state = TetrisArea(size=(8, 4), cells=cells)
    assert state.has_completed_line() == expected

@pytest.mark.parametrize("cells, removed, expected", [
    ({}, {}, set()),
    ({(2, 0)}, {0, 1}, {(0, 0)}),
    ({(2, 0), (3, 0)}, {0, 1}, {(0, 0), (1, 0)}),
])
def test_apply_gravity(cells, removed, expected):
    state = TetrisArea(size=(8, 4), cells=cells)
    state.apply_gravity(removed)
    assert state.cells == expected

@pytest.mark.parametrize("cells, lines, expected", [
    ({}, {}, set()),
    ({(1, 0)}, {2}, {(1, 0)}),
    ({(1, 0), (2, 0), (3, 0)}, {2}, {(1, 0), (3, 0)}),
    ({(1, 0), (2, 0), (2, 1), (3, 0)}, {2}, {(1, 0), (3, 0)}),
    ({(2, 0), (2, 1), (2, 2)}, {2}, set())
])
def test_remove_cells_by_line(cells, lines, expected):
    state = TetrisArea(size=(8, 4), cells=cells)
    assert state.remove_cells_by_line(lines) == expected


