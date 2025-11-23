from uniform_random import uniform_random
from Connect_4_Board import Connect4Tree
from MCTS import pmcgs


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

    game(player1=uniform_random, player2=uniform_random)