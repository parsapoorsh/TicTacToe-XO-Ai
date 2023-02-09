from copy import copy
from enum import IntEnum
from functools import lru_cache
from math import inf, ceil
from typing import Tuple, Iterable, Union


class PLAYERS(IntEnum):
    X = -1
    O = 1
    __str__ = __repr__ = lambda self: self.name


# noinspection PyUnresolvedReferences
class Board(list):
    __all__ = ('ai_move', 'empty_cells', 'cell_for_check', 'move', 'is_win', 'is_tie', 'is_end', 'clear', 'copy')

    def __init__(self, size: int = 3):
        self.size = size
        super().__init__([None] * size * size)

    @property
    def turn(self) -> int:
        """it tells which player's turn it is to move next"""
        if self.count(None) % 2 == 1:
            return PLAYERS.X
        return PLAYERS.O

    @staticmethod
    @lru_cache
    def cell_for_check(n):
        reuslt = []
        reuslt.extend(tuple(i + ii - 1 for i in range(1, n * n + 1, n)) for ii in range(n))  # -
        reuslt.extend(tuple(i + ii - 1 for i in range(n)) for ii in range(1, n * n + 1, n))  # |
        reuslt.append(tuple(i * n - (n - i) - 1 for i in range(1, n + 1)))  # \
        reuslt.append(tuple(i * n - (i - 1) - 1 for i in range(1, n + 1)))  # /
        return tuple(reuslt)

    def empty_cells(self) -> Iterable[int]:
        return [i for i in range(self.size * self.size) if self[i] is None]

    # TODO: make it async
    def ai_move(self, player: int) -> Tuple[int, Union[float, int]]:
        """Move the player with AI, returns move, score, depth"""
        assert not self.is_end(), 'Game is End'
        best_score = -inf
        best_move = None

        if self.count(None) == self.size * self.size:
            # if start first, use centeral cell
            best_move = ceil(self.size / 2) * self.size - (self.size - ceil(self.size / 2)) - 1
            self[best_move] = player
            return best_move, inf

        for key in self.empty_cells():
            self[key] = player
            score: int = self.alpha_beta(player)
            self[key] = None
            if score > best_score:
                best_score = score
                best_move = key
            if score == 1:  # if is win move, break the loop
                break

        self[best_move] = player
        return best_move, best_score

    def move(self, key: int, player: int):
        assert self.turn == player, f'Its not {player} turn'
        key -= 1
        assert self[key] is None, 'Bad cell'
        self[key] = player
        return self

    def alpha_beta(
            self,
            player: int,
            alpha: Union[int, float] = -inf,
            beta: Union[int, float] = inf,
            is_max: bool = False
    ) -> int:
        if self.is_win(player):  # win
            return 1
        elif self.is_win(-player):  # lose
            return -1
        elif self.is_tie():  # tie
            return 0

        if is_max:
            best_score = -inf
            for key in self.empty_cells():
                self[key] = player
                score = self.alpha_beta(player, alpha, beta, False)
                self[key] = None
                if score > best_score:
                    best_score = score
                if score > alpha:
                    alpha = score
                if beta <= alpha:
                    break
            return best_score
        else:
            worst_score = inf
            for key in self.empty_cells():
                self[key] = -player
                score = self.alpha_beta(player, alpha, beta, True)
                self[key] = None
                if score < worst_score:
                    worst_score = score
                if score < beta:
                    beta = score
                if beta <= alpha:
                    break
            return worst_score

    def is_win(self, player: int) -> bool:
        for row in self.cell_for_check(self.size):
            if all(self[i] == player for i in row):
                return True
        return False

    is_tie: bool = lambda self: self.count(None) == 0
    is_end: bool = lambda self: self.is_tie() or self.is_win(PLAYERS.O) or self.is_win(PLAYERS.X)

    def clear(self):
        """Clear the board."""
        super().__init__([None] * self.size * self.size)

    def copy(self):
        """Return a shallow copy of the board."""
        return copy(self)

    def __repr__(self) -> str:
        split_row = f'+{"-" * 3 }' * self.size + '+\n'
        assets = {**PLAYERS._value2member_map_, None: ' '}
        result = split_row
        for i in range(0, self.size * self.size, self.size):
            row = [f"{assets[i]:^3}" for i in self[i: i + self.size]]
            result += f"|{'|'.join(row)}|\n{split_row}"
        return result[:-1]
