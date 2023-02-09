# TicTacToe-XO-Ai
The best Tic Tac Toe move generator with alpha beta pruning algorithm (improved minimax) with many features

## Ai Move
``` python
>>> board.move(5, players.X) # human player
+---+---+---+
| O | X |   |
+---+---+---+
|   | X |   |
+---+---+---+
|   |   |   |
+---+---+---+
>>> board.ai_move(players.O) # move, score, depth
(7, 0, 2)
>>> board
+---+---+---+
| O | X |   |
+---+---+---+
|   | X |   |
+---+---+---+
|   | O |   |
+---+---+---+
```

## Unlimited board
### `3x3`, `4x4`, `NxN` boards can be made
``` python
>>> Board(3)
+---+---+---+
|   |   |   |
+---+---+---+
|   |   |   |
+---+---+---+
|   |   |   |
+---+---+---+
>>> Board(4)
+---+---+---+---+
|   |   |   |   |
+---+---+---+---+
|   |   |   |   |
+---+---+---+---+
|   |   |   |   |
+---+---+---+---+
|   |   |   |   |
+---+---+---+---+
```

## TODO
- [ ] add max_depth to ai_move
- [ ] ai_move using multiple cores
