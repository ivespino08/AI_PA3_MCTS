import numpy as np
from random import randint

class Connect4Tree:

    def __init__(self):
        self.board = np.full((6,7),"O")
        self.moves = 0

    def drop(self, column, color):
        i = 0
        while i < len(self.board) and self.board[i][column] == "O":
            i += 1

        if i == 0:
            self.column_full(column+1)
            return False, False
        
        self.board[i-1][column] = color
        self.moves += 1

        did_win = self.check_win(color, (i-1, column))
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
    token_dropped = False
    did_win = False
    while not token_dropped:
        col_chosen = randint(0, len(board.board[0])-1)
        token_dropped, did_win = board.drop(col_chosen, color)
        
    return did_win

    
def game(player1, player2):
    board = Connect4Tree()
    print(board.board)

    while True:


        if player1(board, "Y"):
            print("\nPlayer 1 has won!")
            break
        print("\nPlayer 1 move:")
        print(board.board)

        if board.is_full():
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

    game(uniform_random, uniform_random)
    

    
    