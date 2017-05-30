class Board(object):
    #  basically this is a constructor
    def __init__(self):
        self.board = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]


    def printboard():
        print(my_board.board[0][0] + "|" + my_board.board[0][1] + "|" + my_board.board[0][2])
        print(my_board.board[1][0] + "|" + my_board.board[1][1] + "|" + my_board.board[1][2])
        print(my_board.board[2][0] + "|" + my_board.board[2][1] + "|" + my_board.board[2][2])

    #Make this method
    def Win():
        #check for win
        boardWin = False

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
    return turn

    # at the end of each turn print the board
    Board.printboard()

# Main Method run the game
def main():
    print("*****************Welcome to TicTacToe******************\n")
    #Create turns
    aTurn = Turn()
    current_turn = aTurn.X
    while(Board.Win() != False):
        input_row = input("Player " + current_turn +" Enter Row number: ")
        input_col = input("Player " + current_turn + " Enter Column number: ")

        #place piece on board
        my_board.board[int(input_row)][int(input_col)] = current_turn
        current_turn = changeTurn(current_turn)
        Board.printboard()



#run the main method
if __name__ == '__main__':
    main()
