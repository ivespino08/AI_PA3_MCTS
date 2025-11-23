from random import choice
from Connect_4_Board import Connect4Tree


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

