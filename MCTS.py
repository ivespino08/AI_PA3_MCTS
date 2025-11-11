import numpy as np
from random import randint

class Connect4Tree:

    def __init__(self):
        self.board = np.full((6,7),"O")

    def drop(self, column, color):

        i = 0
        while i < len(self.board) and self.board[i][column] == "O":
            i += 1

        self.board[i-1][column] = color





def uniform_random(board):
    col_chosen = randint(0, len(board.board[0])-1)
    board.drop(col_chosen, "Y")
    

if __name__ == "__main__":
    ct = Connect4Tree()
    uniform_random(ct)

    print(ct.board)
    