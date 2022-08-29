from functools import lru_cache
from copy import copy
from typing import Tuple, List, Iterable, Union
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

    def ai_move(self, player: int) -> Tuple[int, Union[int, float], int]:
        """Move the player with ai, returns move, score, depth"""
        assert not self.is_end(), 'Game is End'
        best_score = -inf
        best_move = None

        r = self.evaluate(player)
        for key, score in r.items():
            if score >= best_score:
                best_score = score
                best_move = key
        
        self[best_move] = player
        return best_move, best_score

    def move(self, key: int, player: int):
        key -= 1
        assert self[key] == None, 'Bad cell'
        self[key] = player
        return self

    def evaluate(self, player: int) -> dict:
        result = {i: 0 for i in self.empty_cells()}
        for row in self.cell_for_check(self.size):
            for i in row:
                if i not in self.empty_cells():
                    continue
                if any(self[i] == players.O for i in row) and \
                   any(self[i] == players.X for i in row):
                    continue
                
                self[i] = -player
                if self.is_win(players.X) or self.is_win(players.O):
                    result[i] = inf
                else:
                    result[i] += 1
                self[i] = None
        return result
    
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
    ai_player = players.X
    while 1:
        t1 = time()
        move, score = board.ai_move(ai_player)
        t2 = time()
        tT = round(t2-t1, 3)
        print(f'move: {move+1}, {tT}s', board, sep='\n')

        if not board.is_end():
            board.move(int(input('Human move: ')), -ai_player)

        if board.is_end():
            print(
                'Game is end,',
                'Tie' if board.is_tie() else
                'X Win' if board.is_win(players.X) else
                'O Win'
            )
            board.clear()
            break
