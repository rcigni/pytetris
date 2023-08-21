from enum import Enum, auto
from typing import Callable

from pytetris.logic.gen_logic import RandomLogic, GenLogic
from pytetris.logic.loc_tetrimino import LocTetrimino
from pytetris.logic.tetriminos import TO, TTs, new_tetrimino_by_type, Tetrimino
from pytetris.logic.tetris_state import TetrisArea
from pytetris.logic.tetris_stats import GameStats


class GameStatus(Enum):
    GAME_READY = auto()
    GAME_ON = auto()
    GAME_OVER = auto()


class TetrisGame:

    def __init__(self, area: TetrisArea,
                 falling_tetrimino: LocTetrimino = None,
                 gen_logic: GenLogic = RandomLogic(TTs),
                 on_game_over: Callable[[GameStats], None] = lambda: None,
                 preview_count: int = 3,
                 game_stats: GameStats = GameStats(leaders=[])):
        self.area = area
        self.falling_tetrimino = falling_tetrimino

        self.gen_logic = gen_logic
        self.previews: list[Tetrimino] = []
        self.preview_count = preview_count

        self.on_game_over = on_game_over

        self.game_status = GameStatus.GAME_READY
        self.stats = game_stats

    def next_round(self):
        self.stats.next_turn()
        self.next_move(TO.DOWN)

    def rotate_right(self):
        right = self.falling_tetrimino.rotate_right()
        if self.area.is_free(right):
            self.falling_tetrimino = right

    def next_move(self, orientation: TO) -> bool:
        assert orientation is not TO.UP
        will_move = self.area.will_move(self.falling_tetrimino, orientation)
        if will_move:
            self.falling_tetrimino = self.falling_tetrimino.move(orientation)
        elif orientation == TO.DOWN:
            self.freeze()
            self.add_tetrimino()
        return will_move

    def next_move_until_free(self, orientation: TO) -> None:
        while self.next_move(orientation):
            pass

    def freeze(self):
        completed_lines_count = self.area.add_cells(self.falling_tetrimino)
        self.stats.update_score(completed_lines_count)

    def start_game(self):
        self.game_status = GameStatus.GAME_ON
        for _ in range(self.preview_count):
            self.previews.append(self.new_rand())
        self.add_tetrimino()

    def add_tetrimino(self):
        piece = self.previews.pop(0)
        self.previews.append(self.new_rand())
        new_loc_piece = LocTetrimino(self.enter_position(), piece)
        if self.area.is_free(new_loc_piece):
            self.stats.update_pieces(1)
            self.falling_tetrimino = new_loc_piece
        else:
            self.game_over()

    def enter_position(self) -> tuple[int, int]:
        return self.area.enter_position()

    def game_over(self):
        self.game_status = GameStatus.GAME_OVER
        self.on_game_over(self.stats)

    def new_rand(self) -> Tetrimino:
        piece_type = self.gen_logic.next()
        piece = new_tetrimino_by_type(piece_type)
        return piece
