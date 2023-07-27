from Board import Board

class TooManyMines(Exception):
    '''Raised when the number of mines exceeds the total available tiles'''
    pass


class InputNotInBounds(Exception):
    '''Raised when the inputted row or column is not in the bounds'''
    pass


def board_setup():

    # Gets inputs for width, ensures it is a positive integer
    correct = False
    while not correct:
        try:
            width = int(input("What is the width? "))
            if width <= 0:
                raise ValueError
            correct = True
        except ValueError:
            print("The height must be a positive integer, try again.")

    # Gets input for height, ensures it is a positive integer
    correct = False
    while not correct:
        try:
            height = int(input("What is the height? "))
            if height <= 0:
                raise ValueError
            correct = True
        except ValueError:
            print("The height must be a positive integer, try again.")

    # Gets input for # of mines, ensures it is a positive integer and ensures that they can fit
    correct = False
    while not correct:
        try:
            mines = int(input("How many mines? "))
            if mines >= width*height:
                raise TooManyMines()
            correct = True
        except TooManyMines():
            print("The total number of mines must be less than the total number of tiles in the board, try again. ")
        except ValueError:
            print("The total number of mines must be a positive integer, try again.")
    returned_board = Board(width, height, mines)
    # returns created board
    return returned_board


def get_choice(inputted_board):
    fgp = input("Do you want to flag a mine (f), guess a tile (g), or toggle between probabilities (p)? ").lower()
    while fgp != 'g' and fgp != 'f':
        if fgp == 'p':
            inputted_board.probabilities = not inputted_board.probabilities
            print(inputted_board)
            fgp = input("Do you want to flag a mine (f), guess a tile (g), or toggle between probabilities (p)? ").lower()
        else:
            print("That is not a valid choice, try again: ")
            fgp = input("Do you want to flag a mine (f), guess a tile (g), or toggle between probabilities (p)? ").lower()
    return fgp


def get_tile_choice(inputted_board):
    correct = False
    while not correct:
        try:
            row = int(input("Which row of the board do you want to check? "))
            if not 0 <= row < inputted_board.height:
                raise InputNotInBounds
            correct = True
        except InputNotInBounds:
            print(f"You must chose a value from 0 to {inputted_board.height - 1}")
        except ValueError:
            print("Your input must be a non-negative integer")

    correct = False
    while not correct:
        try:
            column = int(input("Which column of the board do you want to check? "))
            if not 0 <= column < inputted_board.width:
                raise InputNotInBounds
            correct = True
        except InputNotInBounds:
            print(f"You must chose a value from 0 to {inputted_board.width - 1}")
        except ValueError:
            print("Your input must be a non-negative integer")
    if (row, column) in inputted_board.unknown_neighbors.keys():
        print("That tile has already been uncovered, try again")
        return get_tile_choice(inputted_board)
    return (row, column)


def decide_outcome(finished_board):
    # Reveals the true values of all the mines
    for i in range(finished_board.height):
        for j in range(finished_board.width):
            if not finished_board.board[i][j].uncovered and finished_board.board[i][j].is_mine:
                finished_board.board[i][j].uncovered = True
    print(finished_board)

    # Determines whether you won or lost
    if len(finished_board.unknown_neighbors) == finished_board.tiles - finished_board.num_mines:
        print("CONGRATULATIONS!!! YOU WON!!")
    else:
        print("You lost")