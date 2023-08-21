from typing import Callable

import arcade

from pytetris.logic.tetris_stats import GameStats


class TetrisLeaderBoard:

    def __init__(self,
                 position: tuple[float, float],
                 get_score: Callable[[], GameStats]):
        self.pos = position
        self.get_score = get_score

    def on_draw(self):
        arcade.draw_rectangle_outline(self.pos[0], self.pos[1], 200, 200, arcade.color.WHITE)
        get_score = self.get_score()
        if len(get_score.leaders) > 0:
            current_score = get_score.score
            leader_bars = [(score, False) for score in get_score.leaders]
            leader_bars.append((current_score, True))
            leader_bars.sort(key=lambda x: x[0], reverse=True)

            for ix, (score, is_current) in enumerate(leader_bars[0:10]):
                self.draw_pos(ix, score, leader_bars[0][0], is_current)

    def draw_pos(self, place: int, value: int, max_value: int, is_current: bool):
        pos0 = self.pos[0] - 90 + (place * 20)
        color = arcade.color.RED if is_current else arcade.color.GREEN_YELLOW
        bar_height = 200 * (value / max_value)
        arcade.draw_rectangle_filled(pos0, self.pos[1] - ((200 - bar_height) / 2), 20, bar_height, color)

