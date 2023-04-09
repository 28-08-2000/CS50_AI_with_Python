"""
Tic Tac Toe Player
"""
import copy
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
    x_moves_played=0
    o_moves_played=0

    for i in range(3): #count the moves played by each player
        for j in range(3):
           if board[i][j] == X:
              x_moves_played += 1
           elif board[i][j] == O:
              o_moves_played += 1
    if x_moves_played > o_moves_played :
        return O
    else: 
        return X
   # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    mySet = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                mytuple = (i,j)
                mySet.add(mytuple)
    #mySet = set((i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY ) #making set of tuples
    return mySet
    #raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    #create a deep copy ofthe original board
    deep_copy_ofboard = copy.deepcopy(board)

    #check if action is valid (i,j)
    if action == None:
        raise NameError('the action is none')
    #ELSE
    i = action[0]
    j = action[1]
    if deep_copy_ofboard[i][j] != EMPTY:
        raise NameError('the cell is not empty')
    else: 
       curr_player = player(deep_copy_ofboard)
       deep_copy_ofboard[i][j] = curr_player
       return deep_copy_ofboard

    #raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3): #for straight lines winner
        if(board[i][0] == board[i][1] and board[i][1] == board[i][2]):  #HORIZONTAL LINE
            return board[i][0]
        elif(board[0][i] == board[1][i] and board[1][i] == board[2][i]):  #VERTICAL LINE
            return board[0][i]
   
    #for diagonally line winner
    if(board[0][0] == board[1][1] and board[1][1] == board[2][2]):
        return board[0][0]
    elif(board[2][0] == board[1][1] and board[1][1] == board[0][2]):
        return board[2][0]
    else:
        return None 

    #raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #check if anyone wins then gameover
    winner_player = winner(board)
    if(winner_player != None):
        return True

   #check if all cells filled then gameover
    for i in range(3):  
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True

    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if(winner_player == X):
        return 1
    elif(winner_player == O):
        return -1
    else:
        return 0 
        
    #raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if(terminal(board)):  #if game is over
        return None

    curr_player = player(board) #choose action according to current player
    if curr_player == X:
        optimal_ans = Max_value(board)
        return optimal_ans[0]
    else:
        optimal_ans = Min_value(board)
        return optimal_ans[0]

    #raise NotImplementedError

#INDIRECT RECURSION
def Max_value(board):
    """
    Returns the action that get to the min score from the max scores
    """
    # BASE CONDITION 
    if terminal(board) == True:
        return (None,utility(board))

    optimal_action = None
    optimal_score = float("-inf")
    for action in actions(board):
        optimal_tuple = Min_value(result(board, action))
        if optimal_score < optimal_tuple[1]:     # take the maximal score as optimal score
            optimal_action = action
            optimal_score = optimal_tuple[1]
    # returns a tuple of optimal action and optimal score
    return (optimal_action, optimal_score)


def Min_value(board):
    """
    Returns the action that get to the min score from the max scores
    """
    #base condition 
    if terminal(board) == True:
        return (None,utility(board))

    optimal_action = None
    optimal_score = float("inf")
    for action in actions(board):
        optimal_tuple = Max_value(result(board, action))
        if optimal_score > optimal_tuple[1]:       #take the minimal score as optimal score
            optimal_action = action
            optimal_score = optimal_tuple[1]
    return (optimal_action,optimal_score)     #returns a tuple of optimal action and optimal score

