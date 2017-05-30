class Board:
    #  basically this is a constructor
    def __init__(self):
        self.board = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]


    def printboard(self):
        print(self.board[0][0] + "|" + self.board[0][1] + "|" + self.board[0][2])
        print(self.board[1][0] + "|" + self.board[1][1] + "|" + self.board[1][2])
        print(self.board[2][0] + "|" + self.board[2][1] + "|" + self.board[2][2])

    #Make this method- (unfinished)
    def win(self):
        #check for win
        boardWin = False
        return boardWin

    def is_valid_move(self):
        pass


# create board object
my_board = Board()

class Turn():
     X = "X"
     O = "O"

def __init__(self,X,O):
    self.O = O
    self.X = X

def changeTurn(turn):

    if(turn is Turn.O):
        turn = Turn.X
    elif(turn is Turn.X):
        turn = Turn.O
    my_board.printboard()
    # at the end of each turn print the board
    return turn



# Main Method run the game
def main():
    print("*****************Welcome to TicTacToe******************\n")
    tic_tac_toe = Board()

    #Create turns
    aTurn = Turn()
    current_turn = aTurn.X

    gameOver = tic_tac_toe.win()

    while(gameOver == False):
        input_row = input("Player " + current_turn +" Enter Row number: ")
        input_col = input("Player " + current_turn + " Enter Column number: \n")

        #place piece on board
        my_board.board[int(input_row)][int(input_col)] = current_turn
        #change turns
        current_turn = changeTurn(current_turn)




#run the main method
if __name__ == '__main__':
    main()
