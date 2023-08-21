import random
from typing import Protocol

from pytetris.logic.tetriminos import TT


class GenLogic(Protocol):
    """GenLogic defines the tetrimino generation logic."""
    def next(self) -> TT:
        ...

class BagOfSevenLogic:
    def __init__(self, bag: list[TT]):
        self.bag = bag
        self._next = []

    def next(self) -> TT:
        if len(self._next) == 0:
            self._next = self.bag.copy()
            random.shuffle(self._next)
        return self._next.pop(0)


class RandomLogic:
    def __init__(self, bag: list[TT]):
        self.bag = bag

    def next(self) -> TT:
        return random.choice(self.bag)
