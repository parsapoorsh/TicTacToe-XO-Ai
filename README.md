# TicTacToe-XO-Ai
The best Tic Tac Toe move generator and unlimited board.

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
>>> board.ai_move(players.O) # move, score
(7, 0)
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
