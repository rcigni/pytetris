import math
from dataclasses import dataclass, field

SCORE_TABLE = {
    0: 0,
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}

@dataclass
class GameStats:
    turns: int = 0
    score: int = 0
    pieces: int = 0

    leaders: list[int] = field(default=list[int])

    def next_turn(self):
        self.turns += 1

    def update_score(self, score: int):
        self.score += SCORE_TABLE[score]

    def update_pieces(self, pieces: int):
        self.pieces += pieces

    def get_round_len(self) -> float:
        level = (30 - math.sqrt(self.pieces)) / 30
        return level
