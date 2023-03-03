"""
Tic Tac Toe Player
"""
import math
X = "X"
O = "O"
EMPTY = None


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
    count_of_x, count_of_O = 0,0
    for i in range(3):
        count_of_x += board[i].count(X)
        count_of_O += board[i].count(O)
    if  count_of_x == 0:
         return X
    elif count_of_x <= count_of_O:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.append((i,j))
    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    import copy
    new_board = copy.deepcopy(board)
    if new_board[action[0]][action[1]] == X or new_board[action[0]][action[1]] == 0:
        raise "Invalid action"
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                if j == 0 and board[i][j+1] ==X and board[i][j+2] == X:
                    return X
                elif (i == 0 and board[i+1][j] ==X and board[i+2][j] == X) or (i==j==0 and  board[i+1][j+1] ==X and board[i+2][j+2] == X):
                    return X
                elif (i==0 and j==2) and(i==0 and  board[i+1][j-1] ==X and board[i+2][j-2] == X):
                    return X
            elif board[i][j] == O:
                if j == 0 and board[i][j+1] ==O and board[i][j+2] == O:
                    return O
                elif (i == 0 and board[i+1][j] ==O and board[i+2][j] == O) or (i==j==0 and  board[i+1][j+1] ==O and board[i+2][j+2] == O):
                    return O
                elif (i==0 and j==2) and(i==0 and  board[i+1][j-1] ==O and board[i+2][j-2] == O):
                    return O
    return None     



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    state = winner(board)
    if state is not None:
        return True
    else:
        empty = 0
        for i in range(3):
           empty += board[i].count(EMPTY)
        if empty == 0:
            return True
 
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    possible_actions = actions(board)
    results = []
    m = -1
    if player(board) == X:
        for i in range(len(possible_actions)):
            r = min_value(result(board,possible_actions[i]))
            results.append(r)
        m = max(results)
        
    elif player(board) == O:
        for i in range(len(possible_actions)):
            r = max_value(result(board,possible_actions[i]))
            results.append(r)
        m = min(results)
    return possible_actions[results.index(m)]
def max_value(board):

    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v,min_value(result(board,action)))
    return v
def min_value(board):

    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v,max_value(result(board,action)))
    return v