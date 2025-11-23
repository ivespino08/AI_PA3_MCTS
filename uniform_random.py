from random import randint

def uniform_random(board, color):
    """
    YOUR ALGORITHM 1 (Unchanged)
    Randomly chooses a legal column and drops a token.
    Returns did_win (True/False).
    """
    token_dropped = False
    did_win = False
    while not token_dropped:                                        #Run until a token is successfully dropped
        col_chosen = randint(0, len(board.board[0])-1)
        token_dropped, did_win = board.drop(col_chosen, color)
        
    return did_win