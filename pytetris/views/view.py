from typing import Protocol

import arcade


class View(Protocol):
    def on_draw(self):
        ...


def update_square_piece(form: tuple[float, float], _offset: tuple[float, float], size: float) -> tuple[float, float]:
    x, y = form
    offset_x, offset_y = _offset
    return x + offset_x * size, y + offset_y * size


def draw_abs_blocks(position: tuple[float, float], cells: dict[tuple[int, int], arcade.Color], size: float):
    p_center = update_square_piece(position, (1, 1), size / 2)
    for cell in cells:
        color = cells[cell]
        flip = (cell[1], cell[0])
        p = update_square_piece(p_center, flip, size)
        arcade.draw_rectangle_filled(p[0], p[1], size - 2, size - 2, color)
