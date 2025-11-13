import numpy as np
from random import randint

class Connect4Tree:

    def __init__(self):
        self.board = np.full((6,7),"O")

    def drop(self, column, color):
        i = 0
        while i < len(self.board) and self.board[i][column] == "O":
            i += 1

        if i == 0:
            self.column_full(column+1)
            return False, False
        
        self.board[i-1][column] = color

        did_win = self.check_win(color, (i-1, column))
        return True, did_win

    def column_full(column):
        print(f"Error: Column {column} is full please choose another")

    def check_win(self, color, drop_location):

        #Horizontal Check
        consecutive = 1
        left, right = drop_location[0]

        while left >= 0 and consecutive < 4:
            if self.board[left][drop_location[1]] != color:
                break
            consecutive += 1
            left -= 1

        while right < len(self.board) and consecutive < 4:
            if self.board[right][drop_location[1]] != color:
                break
            consecutive += 1
            right += 1

        if consecutive >= 4:
            return True 


        #vertical check
        consecutive = 1
        top, bottom = drop_location[1]

        while top < 0 and consecutive < 4:
            if self.board[drop_location[0]][top] != color:
                break
            consecutive += 1
            top -= 0

        while bottom < len(self.board[0]) and consecutive < 4:
            if self.board[drop_location[0]][bottom] != color:
                break
            consecutive += 1
            bottom += 1

        if consecutive == 4:
            return True
                
        #Diagonal check
        consecutive = 0
                    
        

        return False






def uniform_random(board):
    while True:

        token_dropped = False
        while not token_dropped:
            col_chosen = randint(0, len(board.board[0])-1)
            token_dropped, did_win = board.drop(col_chosen, "Y")

            if token_dropped and did_win:
                break

    
    

if __name__ == "__main__":
    ct = Connect4Tree()
    uniform_random(ct)

    print(ct.board)
    