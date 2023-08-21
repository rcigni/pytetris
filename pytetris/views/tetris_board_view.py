from typing import Callable

import arcade

from pytetris.logic.tetris_game import TetrisGame, GameStatus
from pytetris.views.view import draw_abs_blocks


class TetrisBoardView:
    """ Tetris View. Draw the board and the current piece.
    it requires a position in space and a size to be rendered.

    get_game is a function that returns the game to be rendered: in this way we can change the game during the execution
    and the view will be updated automatically.

    It implements the View protocol, so it can be used by the Controller. ""
    """

    def __init__(self, position: tuple[float, float], get_game: Callable[[], TetrisGame], size: float = 25):
        self.position = position
        self.get_game = get_game
        self.size = size

    @property
    def game(self):
        return self.get_game()

    def on_draw(self):
        self.draw_borders()
        if self.game.falling_tetrimino:
            self.draw_blocks(self.game.falling_tetrimino.squares_and_color())
        if self.game.game_status == GameStatus.GAME_ON:
            self.draw_stats(600, 12)
        self.draw_blocks(self.game.area.cells_and_colors())
        if self.game.game_status == GameStatus.GAME_OVER:
            arcade.draw_text("GAME OVER", self.position[0], self.position[1] + 100, arcade.color.RED, 36)

    def draw_blocks(self, cells: dict[tuple[int, int], arcade.Color]):
        draw_abs_blocks(self.position, cells, self.size)

    def draw_stats(self, start_x: int, font_size:int):
        texts = [
            f"{self.game.stats.score} Scores {self.game.stats.pieces} Pieces",
            f"{self.game.stats.turns} Turn {self.game.stats.get_round_len():.2f} Speed ",
        ]
        for ix, text in enumerate(texts):
            arcade.draw_text(text, start_x, 600 - (ix * font_size * 2), arcade.color.WHITE, font_size, width=200, align="center")

    def draw_borders(self):
        height = self.game.area.size[0] * self.size
        width = self.game.area.size[1] * self.size
        lines = [
            (self.position[0], self.position[1] + height),
            (self.position[0], self.position[1]),
            (self.position[0], self.position[1]),
            (self.position[0] + width, self.position[1]),
            (self.position[0] + width, self.position[1]),
            (self.position[0] + width, self.position[1] + height),
        ]
        arcade.draw_lines(lines, arcade.color.WHITE, 1)

        soft_lines = []
        for i in range(1, self.game.area.size[1]):
            soft_lines.append((self.position[0] + self.size * i, self.position[1] + height))
            soft_lines.append((self.position[0] + self.size * i, self.position[1]))

        for i in range(1, self.game.area.size[0]):
            soft_lines.append((self.position[0] + width, self.position[1] + self.size * i))
            soft_lines.append((self.position[0], self.position[1] + self.size * i))

        arcade.draw_lines(soft_lines, arcade.color.GRAY, 0.5)



