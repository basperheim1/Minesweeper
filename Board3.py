import random
from Tile import Tile
from RandomFunctions import random_sample_with_exclusion, combinations
from math import factorial

class Board:
    def __init__(self, height, width, num_mines, first_row, first_column):

        # Sets up the basics of the game
        self.height = height
        self.width = width
        self.num_mines = num_mines
        self.tiles = height * width
        self.probabilities = False
        self.board = []

        # Creates various data structures to help keep track of how the game is progressing
        self.known_mines = set()
        self.tiles_with_data = set()
        self.clicked_tiles = set()
        self.known_tiles = set()

        # This is the most important part of the probability determining process, the 4 sets above are used to help configure this list
        # This list, will become a list of lists, with each sub-list being a possible combination of mines
        # These sublists will only contain tiles adjacent to clicked tiles, that have not been clicked themselves, and are undetermined
        # An undetermined tile refers to a tile that, given the current data, could or could not have a mine underneath it
        # Tiles that are determined, either by being clicked or being 100% a mine or 0% a mine, will not be in this list
        self.islands = []

        # Randomly determines where the mines should be located
        self.mine_locations = random_sample_with_exclusion(0, self.tiles-1, first_row*width+first_column, num_mines)
        for i in range(height):
            self.board.append([])
            for j in range(width):
                if i*width+j == self.mine_locations[-1]:
                    self.board[i].append(Tile(True))
                    self.mine_locations.pop()
                else:
                    self.board[i].append(Tile(False))

        # For each tile object, determines how many mines are around it, and what other tiles are around it
        for i in range(height):
            for j in range(width):
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if 0 <= i + k < self.height and 0 <= j + l < self.width and not k == l == 0:
                            self.board[i][j].surrounding_tiles.add((i+k, j+l))
                            if self.board[i+k][j+l].is_mine:
                                self.board[i][j].mines_around += 1

        # clicks the first tile           
        self.tile_clicked(first_row, first_column)

    # If a given tile is determined to be a mine, that tile is added to the mines set.
    # Additionally, for each tile adjacent to the mine, the number of known mines goes up by 1 and the original tile is added to the known_tiles set
    # Also, the tile determined to be a mine is removed from all possible mine combinations
    def mine_known(self, row, column):
        self.known_mines.add((row, column))
        for i in self.board[row][column].surrounding_tiles:
            self.board[i[0]][i[1]].known_tiles.add((row, column))
            self.board[i[0]][i[1]].tile_known_mines += 1
        for i in self.islands:
            i.remove((row, column))


    # Executes when a tile has been clicked. 
    # Additionally, for each tile adjacent to the clicked tile, the clicked tile is added to the known_tiles set of the adjacent tile
    # Also, the clicked tile is removed from all possible mine combinations
    def tile_known(self, row, column):
        for i in self.board[row][column].surrounding_tiles:
            self.board[i[0]][i[1]].known_tiles.add((row, column))

        for i in self.islands:
            if (row, column) in i[1]:
                for j in i[2]:
                    if (row, column) in j:
                        i[2].remove(j)

    # Overrides the string method for the board
    def __str__(self):

        # Formats the first row of the board, which is just a list of numbesr from 1 to self.width
        formatted_string = '     1'
        for i in range(2, self.width+1):
            if i > 9:
                formatted_string += f'   {i}'
            else:
                formatted_string += f'    {i}'
        formatted_string += '\n'

        # Formats the next self.height rows. The format for these rows are: {row number} [   ][   ][   ] ... [   ]
        for idx, i in enumerate(self.board):
            if idx+1 > 9:
                formatted_string += str(idx+1) + ' '
            else:
                formatted_string += ' ' + str(idx+1) + ' '

            # Determines whether or not to display the probabilities
            if self.probabilities:
                for j in i:
                    formatted_string += j.prob_str()
                formatted_string += '\n'
            else:
                for j in i:
                    formatted_string += j.no_prob_str()
                formatted_string += '\n'

        return formatted_string
            
                
    # Executes when a given tile is clicked
    def tile_clicked(self, row, column):
        if self.board[row][column].uncovered:
            pass

        # The clicked tile is uncovered, and added to the tiles_with_data set, the checked_tiles set, and the known_tiles set
        # The tiles surrounding the clicked tile are added to the tile_with_data set
        else:
            self.board[row][column].uncovered = True
            self.tile_known(row, column)
            self.tiles_with_data.add((row, column))
            self.clicked_tiles.add((row, column))
            self.known_tiles.add((row, column))
            self.tiles_with_data.update(self.board[row][column].surrounding_tiles)

            # If the clicked tile is a mine, then the game is over, otherwise, the possible mine combinations are updated, and the surrounding tiles are checked
            if self.board[row][column].is_mine:
                return False
            else:
                self.determine_combos(row, column)
                self.check_surrounding(row, column)
                return True

    # If the clicked tile has 0 mine around it, then all the tiles adjacent to the clicked tile are also clicked. 
    def check_surrounding(self, row, column):
        if self.board[row][column].mines_around == 0:
            for i in self.board[row][column].surrounding_tiles:
                self.tile_clicked(i[0], i[1])

    # This is where the possible combinations of mines are determined.
    # This method is called each time a new tile has been clicked, as more data has been gathered
    def determine_combos(self, row, column):

        index = []
        for idx, i in enumerate(self.islands):
            for j in list(self.board[row][column].surrounding_tiles) + [(row, column)]:
                if j in i[1]:
                    index.append(idx)
                    break

        # The tile_mine_combos represents all the combinations of undetermined tiles around the clicked tile
        # For example if there are 3 undetermined tiles, and one undetermined mine, there are 3 possible combinations of which undetermined tile is the undetermined mine
        tile_mine_combos = list(combinations(self.board[row][column].surrounding_tiles.difference(self.board[row][column].known_tiles), self.board[row][column].mines_around-self.board[row][column].tile_known_mines))

        if self.islands == []:
            all_surrounding = self.board[row][column].surrounding_tiles.union(set([(row, column)]))
            self.islands = [[set([(row, column)]), all_surrounding, tile_mine_combos]]

        else:

            if index:
                self.islands[index[0]][0].add((row, column))
                self.islands[index[0]][1].update(self.board[row][column].surrounding_tiles)
                self.islands[index[0]][1].add((row, column))
                self.islands[index[0]][2] = [set(x+y) for x in self.islands[index[0]][2] for y in tile_mine_combos]
                self.islands[index[0]][2] = set(map(frozenset, self.islands[index[0]][2]))
                self.islands[index[0]][2] = [list(s) for s in self.islands[index[0]][2]]

                # Determines which of these combinations are actually valid 
                self.islands[index[0]][2][:] = [combo for combo in self.islands[index[0]][2] if self.check_combination(combo, index[0])]

            else:
                all_surrounding = self.board[row][column].surrounding_tiles.union(set([(row, column)]))
                self.islands.append([set([(row, column)]), all_surrounding, tile_mine_combos])


        if len(index) > 1:
            index.sort(reverse = True)
            for i in index[:-1]:
                self.islands[index[-1]][0].update(self.islands[i][0])
                self.islands[index[-1]][1].update(self.islands[i][1])
                self.islands[index[-1]][2] = [set(x+y) for x in self.islands[index[-1]][2] for y in self.islands[i][2]]
                self.islands[index[-1]][2] = set(map(frozenset, self.islands[index[-1]][2]))
                self.islands[index[-1]][2] = [list(s) for s in self.islands[index[-1]][2]]
                self.islands[index[-1]][2][:] = [combo for combo in self.islands[index[-1]][2] if self.check_combination(combo, index[-1])]

            for i in index[:-1]:
                del self.islands[i]

            

    # Checks whether the combinations in the overall board_mine_combos actually work 
    def check_combination(self, combo, idx):
        # If theres more unnaccounted for mines than unnacounted for tiles, then the combination is not valid
        if self.num_mines - (len(combo) + len(self.known_mines)) > self.tiles - len(self.islands[idx][1]):
            return False
        
        # If the number of possible mines is greater than the number of mines, then the combination is not valid 
        if len(combo) + len(self.known_mines) > self.num_mines:
            return False
        
        # If, for each clicked tile, the number of possible mines surrounding each clicked tile does not equal the number of mines surrounding each tile, then the combination is not valid
        for i in self.islands[idx][0]:
            if sum([1 for j in self.board[i[0]][i[1]].surrounding_tiles.difference(self.board[i[0]][i[1]].known_tiles) if j in combo]) != self.board[i[0]][i[1]].mines_around - self.board[i[0]][i[1]].tile_known_mines:
                return False
            
        return True

    # This determines the probabilities, determines it based off of the overall board_mine_combos
    def check_probabilities(self):
        total_combinations = 0
        possible_mines = {}

        # Determines for each sub-list in board_mine_combos, how many total board-wide possible combinations are possible given this sub-list combination is true
        # The sub-lists in board_mine_combos only refer to the tiles adjacent to clicked tiles
        # This loop determines the TOTAL number of combinations, assuming the sub-list combination is correct
        # Helpful link to the underlying calculations of it all: 
        for i in self.islands:
            total_mines_left = self.num_mines - (len(i) + len(self.known_mines))
            total_tiles_left = self.tiles - len(self.tiles_with_data)
            partial_combinations = factorial(total_tiles_left)/(factorial(total_tiles_left-total_mines_left)*factorial(total_mines_left))
            total_combinations += partial_combinations
            for j in i:
                if j in possible_mines:
                    possible_mines[j] += partial_combinations
                else:
                    possible_mines[j] = partial_combinations

        # Determines the probability of there being a mine in each tile
        # Does this by taking all the possible combos with the tile being a mine / all the possible combos
        for k in possible_mines:
            possible_mines[k] = possible_mines[k] / total_combinations

        # Assigns probabilities to tile objects 
        # Adds known tiles to the known_tiles set
        for i in self.tiles_with_data.difference(self.known_tiles):
            self.board[i[0]][i[1]].has_some_data = True
            if i in possible_mines.keys():
                self.board[i[0]][i[1]].probability = possible_mines[i]
                if self.board[i[0]][i[1]].probability == 1:
                    self.known_tiles.add((i[0], i[1]))
                    self.mine_known(i[0], i[1])
            else:
                self.board[i[0]][i[1]].probability = 0
                self.known_tiles.add((i[0], i[1]))
        
