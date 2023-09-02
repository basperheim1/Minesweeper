from BoardSetup import board_setup, get_choice, get_tile_choice, decide_outcome, get_game_type
from Board import Board
import time

game_type = get_game_type()
board = board_setup()
if game_type == 'p':

    keep_going = len(board.clicked_tiles) != board.tiles-board.num_mines

    # While the game has not finished

    while keep_going and board != False:
        board.determine_probabilities()
        print(board)

        # Determines if it's a guess, a flag, or a probability request, then gets the tile location
        choice = get_choice(board)
        tile_location = get_tile_choice(board)

        # Either checks if the tile is a mine, or places a flag
        if choice == 'g':
            keep_going = board.tile_clicked(tile_location[0], tile_location[1])
        else:
            board.board[tile_location[0]][tile_location[1]].flagged = True

        # If all non-mine tiles have been uncovered, the game ends
        if len(board.clicked_tiles) == board.tiles-board.num_mines:
            keep_going = False

    decide_outcome(board)

else:

    board.probabilities = True

    # Checks to see if all non-mine tiles have been clicked
    keep_going = len(board.clicked_tiles) != board.tiles-board.num_mines

    # While the game has not finished

    while keep_going and board != False:
            board.determine_probabilities()
            print(board)
            time.sleep(1)
            lowest_prob_guess = board.determine_ai_choice()
            keep_going = board.tile_clicked(lowest_prob_guess[0], lowest_prob_guess[1])
            if len(board.clicked_tiles) == board.tiles-board.num_mines:
                keep_going = False

    decide_outcome(board)
