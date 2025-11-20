import numpy as np
from random import randint, choice

class Connect4Tree:

    def __init__(self):
        self.board = np.full((6,7),"O")
        self.moves = 0                                                  #Keep track of the total number of moves made this game

    def drop(self, column, color):
        i = 0
        while i < len(self.board) and self.board[i][column] == "O":     #Find the lowest occupied row in the given column
            i += 1

        if i == 0:                                                      #If the column is full, display message and try again
            self.column_full(column+1)
            return False, False
        
        self.board[i-1][column] = color                                 #Drop the token in the row above the lowest occupied
        self.moves += 1

        did_win = self.check_win(color, (i-1, column))                  #Look around the token in all directions to see if player won
        return True, did_win

    def column_full(self, column):
        print(f"Error: Column {column} is full please choose another")

    def check_win(self, color, drop_location):

        #Horizontal Check
        consecutive = 1
        left = drop_location[1] - 1
        right = drop_location[1] + 1

        while left >= 0 and consecutive < 4:
            if self.board[drop_location[0]][left] != color:
                break
            consecutive += 1
            left -= 1

        while right < len(self.board[0]) and consecutive < 4:
            if self.board[drop_location[0]][right] != color:
                break
            consecutive += 1
            right += 1

        if consecutive >= 4:
            return True 


        #Vertical Check
        consecutive = 1
        top = drop_location[0] - 1
        bottom = drop_location[0] + 1

        while top >= 0 and consecutive < 4:
            if self.board[top][drop_location[1]] != color:
                break
            consecutive += 1
            top -= 1

        while bottom < len(self.board) and consecutive < 4:
            if self.board[bottom][drop_location[1]] != color:
                break
            consecutive += 1
            bottom += 1

        if consecutive >= 4:
            return True
                
        #Diagonal Check 1 (top left to bottom right)
        consecutive = 1
        left = drop_location[1] - 1
        right = drop_location[1] + 1
        top = drop_location[0] - 1
        bottom = drop_location[0] + 1

        while top >= 0 and left >= 0 and consecutive < 4:
            if self.board[top][left] != color:
                break
            consecutive += 1
            left -= 1
            top -= 1

        while bottom < len(self.board) and right < len(self.board[0]) and consecutive < 4:
            if self.board[bottom][right] != color:
                break
            consecutive += 1
            right += 1
            bottom += 1

        if consecutive >= 4:
            return True
        

        #Diagonal Check 2 (bottom left to top right)
        consecutive = 1
        left = drop_location[1] - 1
        right = drop_location[1] + 1
        top = drop_location[0] - 1
        bottom = drop_location[0] + 1

        while top >= 0 and right < len(self.board[0]) and consecutive < 4:
            if self.board[top][right] != color:
                break
            consecutive += 1
            right += 1
            top -= 1

        while bottom < len(self.board) and left >= 0 and consecutive < 4:
            if self.board[bottom][left] != color:
                break
            consecutive += 1
            left -= 1
            bottom += 1

        if consecutive >= 4:
            return True
                        
        return False

    def is_full(self):
        if self.moves >= (len(self.board) * len(self.board[0])):
            return True
        
        return False



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




# ============================================================
#        ALGORITHM 2 – PURE MONTE CARLO GAME SEARCH (PMCGS)
# ============================================================

def pmcgs_terminal_check(board_obj):
    """
    Fully checks the board for
        +1 Yellow win
        -1 Red win
         0 Draw
        None game not finished yet
    """
    board = board_obj.board  
    ROWS, COLS = 6, 7
    b = board.tolist()

    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            four = b[r][c:c+4]
            if four == ["Y"] * 4: return 1
            if four == ["R"] * 4: return -1

    # Vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            if b[r][c] == b[r+1][c] == b[r+2][c] == b[r+3][c] == "Y": return 1
            if b[r][c] == b[r+1][c] == b[r+2][c] == b[r+3][c] == "R": return -1

    # Diagonal down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if b[r][c] == b[r+1][c+1] == b[r+2][c+2] == b[r+3][c+3] == "Y": return 1
            if b[r][c] == b[r+1][c+1] == b[r+2][c+2] == b[r+3][c+3] == "R": return -1

    # Diagonal up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if b[r][c] == b[r-1][c+1] == b[r-2][c+2] == b[r-3][c+3] == "Y": return 1
            if b[r][c] == b[r-1][c+1] == b[r-2][c+2] == b[r-3][c+3] == "R": return -1

    # Draw?
    if board_obj.is_full():
        return 0

    return None



def pmcgs_rollout(board_obj, player):
    """
    Runs a full random simulation from the current board
    until a terminal state is reached.
    """
    sim = Connect4Tree()
    sim.board = board_obj.board.copy()
    sim.moves = board_obj.moves

    current = player  

    while True:
        terminal = pmcgs_terminal_check(sim)
        if terminal is not None:
            return terminal

        legal = []
        for c in range(7):
            if sim.board[0][c] == "O":
                legal.append(c)

        move = choice(legal)
        sim.drop(move, current)

        current = "R" if current == "Y" else "Y"



def pmcgs(board, color, simulations=50):
    """
    ALGORITHM 2: PURE MONTE CARLO GAME SEARCH
    This replaces uniform_random as a stronger AI.
    Returns:
        did_win (True/False) ← for compatibility with game loop
    """

    # STEP 1: Get legal moves
    legal_moves = []
    for c in range(7):
        if board.board[0][c] == "O":
            legal_moves.append(c)

    move_scores = {}  # col → average simulation value

    # STEP 2: Evaluate each move using Monte Carlo
    for move in legal_moves:
        total = 0

        for _ in range(simulations):

            # Copy board
            sim_board = Connect4Tree()
            sim_board.board = board.board.copy()
            sim_board.moves = board.moves

            # Try this move
            success, did_win = sim_board.drop(move, color)

            if did_win:
                total += 1 if color == "Y" else -1
                continue

            next_player = "R" if color == "Y" else "Y"
            result = pmcgs_rollout(sim_board, next_player)
            total += result

        avg = total / simulations
        move_scores[move] = avg
        print(f"Column {move+1}: {avg:.3f}")

    # STEP 3: Select best move
    if color == "Y":
        best = max(move_scores, key=move_scores.get)
    else:
        best = min(move_scores, key=move_scores.get)

    print(f"FINAL Move selected: {best+1}")

    # Execute final chosen move on REAL GAME BOARD
    _, did_win_real = board.drop(best, color)
    return did_win_real




# ============================================================
#                       GAME LOOP (UNCHANGED)
# ============================================================

def game(player1, player2):                                 #Takes algorithms as parameters for each player
    board = Connect4Tree()
    print(board.board)

    while True:

        if player1(board, "Y"):
            print("\nPlayer 1 has won!")
            break
        print("\nPlayer 1 move:")
        print(board.board)

        if board.is_full():                                     # If the Board is full end the game
            print("The board is full. It's a tie!")
            break

        if player2(board, "R"):
            print("\nPlayer 2 has won!")
            break
        print("\nPlayer 2 move:")
        print(board.board)

        if board.is_full():
            print("The board is full. It's a tie!")
            break

    print(board.board)
    

if __name__ == "__main__":

    game(player1=pmcgs, player2=uniform_random)
