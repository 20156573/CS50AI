"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

#  my variable
count_step = 0


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    elif count_step % 2 == 0:
        return O
    else:
        return X

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set_actions = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                set_actions.add((i, j))
    return set_actions

    # raise NotImplementedError
board = [[X, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]]
def export():
    action = (1, 2)
    if board[action[0]][action[1]] == EMPTY:
        raise NotImplementedError('Action is not a valid action for the board')
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == X:
                print(" X ", end='')
            elif board[i][j] == O:
                print(" O ", end='')
            else:
                print("({i}, {j})".format(i = i, j = j), end='')
        print("\n")
    print(actions(board))


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise NotImplementedError('Action is not a valid action for the board')
    else:
        new_board = deepcopy(board)
        new_board[action[0]][action[1]] = player(board)
        return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if count_step < 5:
        return None
    else:

        vertical_value = EMPTY
        horizontal_value = EMPTY

        avg_len = math.ceil(len(board)/2)
        value_between = board[avg_len][avg_len]
        cross_left_value = value_between
        cross_right_value = value_between

        for i in range(len(board)):
            vertical_value = board[0][i]
            horizontal_value = board[i][0]

            # check vertical
            if vertical_value != EMPTY:
                for j in range(len(board) - 1):
                    if board[j + 1][i] != vertical_value:
                        vertical_value = EMPTY
                        break
                if vertical_value != EMPTY:
                    return vertical_value

            # check horizontal
            if horizontal_value != EMPTY:
                for j in range(len(board) - 1):
                    if board[i][j + 1] != horizontal_value:
                        horizontal_value = EMPTY
                        break
                if horizontal_value != EMPTY:
                    return horizontal_value
            
            # check cross
            if value_between != EMPTY:
                cross_left_value = board[i][i]
                cross_right_value = board[i][len(board) - 1 - i]
                if cross_left_value != value_between:
                    cross_left_value = EMPTY
                if cross_right_value != value_between:
                    cross_right_value = EMPTY
        if cross_left_value != EMPTY:
            return cross_left_value
        if cross_right_value != EMPTY:
            return cross_right_value
            
        return None
                

    
    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
