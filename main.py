from BoardSetup import board_setup, get_choice, get_tile_choice, decide_outcome

# Sets up the board
keep_going = True
board = board_setup()
board.determine_combos()
board.check_probabilities(board.possible_combos)
if len(board.unknown_neighbors) == board.tiles-board.num_mines:
    keep_going = False

# While the game has not finished
while keep_going:
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
    if len(board.unknown_neighbors) == board.tiles-board.num_mines:
        keep_going = False
    # board.check_probabilities(board.determine_combos())
    board.determine_combos()
    board.check_probabilities(board.possible_combos)

decide_outcome(board)