from functools import lru_cache
from copy import copy
from typing import Tuple, List, Iterable, Union
from multiprocessing import Pool
from math import inf, ceil

class players():
    X = -1
    O = 1

class Board(list):
    __all__ = ('check', 'ai_move', 'empty_cells', 'cell_for_check', 'score2status', 'move', 'is_win', 'is_tie', 'is_end', 'clear', 'copy')
    def __init__(self, size: int=3):
        self.size=size
        super().__init__([None]*size*size)

    @staticmethod
    @lru_cache
    def cell_for_check(n) -> Tuple[Tuple[int]]:
        reuslt = []
        reuslt.extend(tuple(i+ii-1 for i in range(1, n*n+1, n)) for ii in range(n)) # -
        reuslt.extend(tuple(i+ii-1 for i in range(n)) for ii in range(1, n*n+1, n)) # | 
        reuslt.append(tuple(i*n - (n-i)-1 for i in range(1, n+1)))                  # \
        reuslt.append(tuple(i*n - (i-1)-1 for i in range(1, n+1)))                  # /
        return tuple(reuslt)

    def empty_cells(self) -> Iterable[int]:
        return [i for i in range(self.size*self.size) if self[i] == None]

    def ai_move(self, player: int, max_depth: Union[int, None]=None, multiprocess: bool=True) -> Tuple[int, Union[int, float], int]:
        """Move the player with ai, returns move, score, depth"""
        assert not self.is_end(), 'Game is End'
        best_score = -inf
        best_move = None
        max_depth = max_depth if max_depth != None else self.size*self.size

        if self.count(None) == self.size*self.size:
            # if start first, use centeral cell
            best_move = ceil(self.size/2) * self.size - (self.size - ceil(self.size/2)) -1
            self[best_move] = player
            return best_move, inf, self.size*self.size

        if multiprocess:
            with Pool() as p:
                result = p.starmap(
                    Board.alpha_beta,
                    ((self.copy().move(i+1, player), player, max_depth,) for i in self.empty_cells()),
                )
        else:
            result = map(
                Board.alpha_beta,
                [self.copy().move(i+1, player) for i in self.empty_cells()],
                (player,)*len(self.empty_cells()),
                (max_depth,)*len(self.empty_cells()),
            )
        
        for key, (score, depth,) in zip(self.empty_cells(), result):
            if score > best_score:
                best_score = score
                best_move = key
            if score == 1: # if is win move, break the loop
                break
        
        self[best_move] = player
        return best_move, best_score, max_depth-depth+1

    def move(self, key: int, player: int):
        key -= 1
        assert self[key] == None, 'Bad cell'
        self[key] = player
        return self

    def alpha_beta(
            self,
            player: int,
            depth: int,
            alpha: Union[int, float] = -inf,
            beta: Union[int, float] = inf,
            is_max: bool = False
        )  -> Tuple[int, int]:
        if self.is_win(player): # win
            return 1, depth
        elif self.is_win(-player): # lose
            return -1, depth
        elif self.is_tie() or depth <= 0: # tie
            return 0, depth


        if is_max:
            best_score = -inf
            for key in self.empty_cells():
                self[key] = player
                score, d = self.alpha_beta(player, depth-1, alpha, beta, False)
                self[key] = None
                if score > best_score:
                    best_score = score
                if score > alpha:
                    alpha = score
                if beta <= alpha:
                    break
            return best_score, d
        else:
            worst_score = inf
            for key in self.empty_cells():
                self[key] = -player
                score, d = self.alpha_beta(player, depth-1, alpha, beta, True)
                self[key] = None
                if score < worst_score:
                    worst_score = score
                if score < beta:
                    beta = score
                if beta <= alpha:
                    break
            return worst_score, d

    @staticmethod
    def score2status(score: Union[int, float]) -> str:
        return (
            'tie' if score == 0 else
            'win' if score > 0 else
            'lose'
        )
    
    def is_win(self, player: int) -> bool:
        for row in self.cell_for_check(self.size):
            if all(self[i] == player for i in row):
                return True
        return False
    
    is_tie: bool = lambda self: self.count(None) == 0
    is_end: bool = lambda self: self.is_tie() or self.is_win(players.O) or self.is_win(players.X)

    def clear(self):
        '''Clear the board.'''
        super().__init__([None]*self.size*self.size)
    
    def copy(self):
        '''Return a shallow copy of the board.'''
        return copy(self)

    def __repr__(self) -> str:
        PLAYERS = {players.X: 'X', players.O: 'O', None: ' '}
        ROW = f'+{"-"*3}' * self.size + '+\n'
        string = ROW
        for i in range(0, self.size*self.size, self.size):
            string += '|' + '|'.join(f"{PLAYERS[i]:^3}" for i in self[i: i+self.size]) + f'|\n{ROW}'
        return string[:-1]

if __name__ == '__main__':
    from time import time
    board = Board(3)
    last_player = players.X
    while 1:
        t1 = time()
        move, score, depth = board.ai_move(last_player, multiprocess=False)
        t2 = time()
        tT = round(t2-t1, 3)
        print(
            (
                f'processed depth: {depth}, '
                f'status: {board.score2status(score)}, '
                f'move: {move+1}, '
                f'{tT}s\n'
            ),
            board
        )
        
        last_player = -last_player # convert players
        if board.is_end():
            print(
                'Game is end,',
                'Tie' if board.is_tie() else
                'X Win' if board.is_win(players.X) else
                'O Win'
            )
            #board.clear()
            break
