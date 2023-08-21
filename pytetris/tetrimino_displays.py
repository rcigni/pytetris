import arcade

from pytetris.logic.loc_tetrimino import LocTetrimino
from pytetris.logic.tetriminos import TO, TT, new_tetrimino_by_type
from pytetris.views.tetris_board_view import TetrisBoardView
from pytetris.logic.tetris_game import TetrisGame
from pytetris.logic.tetris_state import TetrisArea


class PiecesWindow(arcade.Window):
    """ View all the """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(50, 50)
        arcade.set_background_color(arcade.color.BLACK)

        size = 12
        board_size: tuple[int, int] = (5, 4)
        board_dim = (board_size[1] * size + (size / 2), board_size[0] * size + (size / 2))

        def _cells(ptype: TT, orientation: TO) -> dict[tuple[int, int], arcade.Color]:
            return LocTetrimino((0, 0), new_tetrimino_by_type(ptype, orientation)).squares_and_color()

        def _pos(col: int, row: int):
            return (col * board_dim[0]) + 50, (row * board_dim[1]) + 50

        def _new_board(position: tuple[float, float], cells: dict[tuple[int, int], arcade.Color]) -> TetrisBoardView:
            game = TetrisGame(TetrisArea(board_size, cells))
            return TetrisBoardView(position, lambda: game, size)

        types = [TT.T, TT.STICK, TT.SQUARE, TT.L1, TT.L2, TT.S1, TT.S2]
        orientations = [TO.UP, TO.RIGHT, TO.DOWN, TO.LEFT]

        self.boards = []
        for it, t in enumerate(types):
            for iori, ori in enumerate(orientations):
                self.boards.append(_new_board(_pos(iori, it), cells=_cells(t, ori)))

    def on_draw(self):
        arcade.start_render()
        for board in self.boards:
            board.on_draw()


PiecesWindow(550, 550, "Tetris")
arcade.run()
