from typing import Callable

from pytetris.logic.loc_tetrimino import LocTetrimino
from pytetris.logic.tetriminos import Tetrimino
from pytetris.views.view import draw_abs_blocks


class TetrisPreview:

    def __init__(self, position: tuple[float, float], get_pieces: Callable[[], list[Tetrimino]], size: float = 25):
        self.position = position
        self.get_pieces = get_pieces
        self.size = size

    def on_draw(self):
        previews = self.get_pieces()
        for ix, preview in enumerate(previews):
            self.draw_blocks(preview, ix)

    def draw_blocks(self, preview: Tetrimino, ix: int):
        offset = ix * 4.5 * self.size
        new_position = (self.position[0], self.position[1] - offset)
        draw_blocks(new_position, preview, self.size)


def draw_blocks(position: tuple[float, float], preview: Tetrimino, size: float = 25):
    cells = LocTetrimino((0, 0), preview).squares_and_color()
    draw_abs_blocks(position, cells, size)
