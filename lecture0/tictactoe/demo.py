import tictactoe

X = "X"
O = "O"
EMPTY = None
board = [[X, X, X],
        [EMPTY, X, EMPTY],
        [X, EMPTY, EMPTY]]
 
print(tictactoe.winner(board))