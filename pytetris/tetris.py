import arcade

from pytetris.sound.background_music import BackgroundMusic
from pytetris.logic.gen_logic import BagOfSevenLogic
from pytetris.logic.scores import read_scores, append_score
from pytetris.logic.tetriminos import TO, TTs
from pytetris.logic.tetris_state import TetrisArea
from pytetris.logic.tetris_stats import GameStats
from pytetris.logic.tetris_game import TetrisGame, GameStatus
from pytetris.views.tetris_leader_board import TetrisLeaderBoard
from pytetris.views.tetris_preview import TetrisPreview
from pytetris.views.view import View
from pytetris.views.tetris_board_view import TetrisBoardView

SCORES_FILE = "leaders.txt"
SQUARE_SIZE = 32

def new_game(leaders: list[int]):
    area = TetrisArea((20, 10), set())

    def on_game_over(stats: GameStats):
        append_score(SCORES_FILE, stats.score)
        leaders.append(stats.score)

    game = TetrisGame(area,
                      gen_logic=BagOfSevenLogic(TTs),
                      on_game_over=on_game_over,
                      game_stats=GameStats(leaders=leaders),
                      )
    return game


class MyTetrisWindow(arcade.Window):
    """ Tetris Controller. intercept the input, update the model and draw the views."""

    def __init__(self, width, height, title):
        # set info for arcade.Window
        super().__init__(width, height, title)
        self.set_location(100, 100)
        arcade.set_background_color(arcade.color.BLACK)

        leaders = read_scores(SCORES_FILE)
        self.game = new_game(leaders)
        self.time = 0

        self.background_music = BackgroundMusic(lambda: self.game.game_status == GameStatus.GAME_ON)

        # create the views and connect them to the model with lambdas  (lazy evaluation)
        self.views: list[View] = [
            TetrisBoardView((50, 50), lambda: self.game, SQUARE_SIZE),
            # preview of next tetriminos (2). this is a stretch in the design because we should use a preview method.
            TetrisPreview((420, 500), lambda: self.game.previews[0:2], SQUARE_SIZE),
            TetrisLeaderBoard((500, 150), lambda: self.game.stats)
        ]

    def on_draw(self):
        arcade.start_render()
        [view.on_draw() for view in self.views]

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        if self.game.game_status == GameStatus.GAME_ON:
            self.time += delta_time
            round_len = self.game.stats.get_round_len()
            if self.time > round_len:
                self.time -= round_len
                self.game.next_round()

        self.background_music.on_update()

    def on_key_press(self, key: int, modifiers: int):
        match self.game.game_status:
            case GameStatus.GAME_ON:
                self.play(key)
            case GameStatus.GAME_READY:
                if key == arcade.key.ENTER:
                    self.game.start_game()
            case GameStatus.GAME_OVER:
                if key == arcade.key.ENTER:
                    self.game = new_game(self.game.stats.leaders)
                    self.time = 0

        match key:
            case arcade.key.S:
                self.background_music.toggle()

    def play(self, key: int):
        match key:
            case arcade.key.UP:
                self.game.rotate_right()
            case arcade.key.RIGHT:
                self.game.next_move(TO.RIGHT)
            case arcade.key.LEFT:
                self.game.next_move(TO.LEFT)
            case arcade.key.DOWN:
                self.game.next_move(TO.DOWN)
            case arcade.key.ENTER:
                self.game.next_move_until_free(TO.DOWN)


MyTetrisWindow(1280, 720, "Tetris")
arcade.run()
