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
        # This list, will become a list of lists, with each sublist having 3 elements
        # Each sublist refers to an "island," and is a section of tiles that are next to one another
        # The first element of these sublists is all the clicked tiles in a given island
        # The second element of these sublists is all the clicked tiles, as well as any tiles adjacent to these clicked tiles
        # The third element of these sublists is another list, which each sub-sublist being a possible configuration of mines around the clicked tiles
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
        self.board[row][column].probability = 1
        self.known_tiles.add((row, column))
        self.known_mines.add((row, column))
        for i in self.board[row][column].surrounding_tiles:
            self.board[i[0]][i[1]].known_tiles.add((row, column))
            self.board[i[0]][i[1]].tile_known_mines += 1
        for i in self.islands:
            if (row, column) in i[1]:
                for j in i[2]:
                    j.remove((row, column))
                break


    # Executes when a tile has been clicked or when a tile is known to not be a mine
    # Additionally, for each tile adjacent to the clicked tile, the clicked tile is added to the known_tiles set of the adjacent tile
    # Also, the clicked tile is removed from all possible mine combinations
    def tile_known(self, row, column):
        if self.board[row][column].probability != 1:
            self.board[row][column].probability = 0
            self.known_tiles.add((row, column))
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

        # Determines which, if any, of the islands the newly clicked tile would be a part of
        index = []
        for idx, i in enumerate(self.islands):
            for j in list(self.board[row][column].surrounding_tiles) + [(row, column)]:
                if j in i[1]:
                    index.append(idx)
                    break

        # The tile_mine_combos represents all the combinations of undetermined tiles around the clicked tile
        # For example if there are 3 undetermined tiles, and one undetermined mine, there are 3 possible combinations of which undetermined tile is the undetermined mine
        tile_mine_combos = list(combinations(self.board[row][column].surrounding_tiles.difference(self.board[row][column].known_tiles), self.board[row][column].mines_around-self.board[row][column].tile_known_mines))

        # If there are no islands, one is made
        if self.islands == []:
            all_surrounding = self.board[row][column].surrounding_tiles.union(set([(row, column)]))
            self.islands = [[set([(row, column)]), all_surrounding, tile_mine_combos]]

        else:

            # If the clicked tile would be part of island(s), then the clicked tile is added to ths island, and the overall island possible mine combinations are adjusted accordingly
            if index:
                self.islands[index[0]][0].add((row, column))
                self.islands[index[0]][1].update(self.board[row][column].surrounding_tiles)
                self.islands[index[0]][1].add((row, column))
                self.islands[index[0]][2] = [set(x+y) for x in self.islands[index[0]][2] for y in tile_mine_combos]
                self.islands[index[0]][2] = set(map(frozenset, self.islands[index[0]][2]))
                self.islands[index[0]][2] = [list(s) for s in self.islands[index[0]][2]]

                # Determines which of these combinations are actually valid 
                self.islands[index[0]][2][:] = [combo for combo in self.islands[index[0]][2] if self.check_combination(combo, index[0])]

            # If the clicked tile is not a part of any islands, a new one is made
            else:
                all_surrounding = self.board[row][column].surrounding_tiles.union(set([(row, column)]))
                self.islands.append([set([(row, column)]), all_surrounding, tile_mine_combos])

        # If the clicked tile would be a part of various islands, these islands are combined
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

            

    # Checks whether the island-level possible combinations of mines actually work
    def check_combination(self, combo, idx):
        # If theres more unnaccounted for mines than unnacounted for tiles, then the combination is not valid
        if self.num_mines - (len(combo) + len(self.known_mines)) > self.tiles - len(self.islands[idx][1]):
            return False
        
        # If the number of possible mines in the island-level combination is greater than the total number of mines, then the combination is not valid 
        if len(combo) + len(self.known_mines) > self.num_mines:
            return False
        
        # If, for each clicked tile in the island, the number of possible mines surrounding each clicked tile does not equal the number of mines surrounding each tile, then the combination is not valid
        for i in self.islands[idx][0]:
            if sum([1 for j in self.board[i[0]][i[1]].surrounding_tiles.difference(self.board[i[0]][i[1]].known_tiles) if j in combo]) != self.board[i[0]][i[1]].mines_around - self.board[i[0]][i[1]].tile_known_mines:
                return False
            
        return True

    # The global frequencies of mines around the islands can be calculated
    # For exmaple, let's say we had 2 islands, and they each had 2 possible configurations of mines
    # Let's say that island1 had the following possible configuration of mines: [(1, 1), (1, 2)] and [(2, 2)]
    # Let's say that island2 had the following possible configuration of mines: [(5, 5), (4, 5)] and [(5, 4)]
    # Then, the global frequencies of mines are as follows: {2: 1, 3: 2, 4: 1}
    # This means that given the island-level possible combinations, then at the global level, there is 1 combination with 2 mines, 2 combinations with 3 mines, and 1 possible combinations with 4 mines
    # This get_glob_one method, uses the global frequences to arrive at the global frequencies, if one of the islands had not existed
    # Inputting the global frequencies, and the island frequencies, results with the global frequencies if that island didn't exist
    # for example, self.get_glob_one({2: 1, 3: 2, 4: 1}, {1:1, 2:1}) would return {1: 1, 2:1}
    def get_glob_one(self, globe, island):
        if len(self.islands) == 1:
            return {0:1}
        glob_one = {}
        while globe:
            index = min(globe.keys()) - min(island.keys())
            ratio = int(globe[min(globe.keys())] / island[min(island.keys())])
            glob_one[index] = ratio
            for i in island:
                globe[index + i] -= island[i]*ratio
                if globe[index + i] == 0:
                    del globe[index + i]
        return glob_one

    # This method determines the global frequencies of mines, which refers to how many times a global possible combination was of x mines was seen
    # This is best seen with an example, consider the following island frequencies (how many times a possible combination of x mines was seen):
    # island1: {2: 3, 3: 2, 4:1}
    # island2: {5:1, 6:2}
    # This means that island1 had 3 possible combinations of mines where the length was 2, 2 possible combinations of mines where the length was 3, and 1 possible combination where the length was 4
    # The global frequency would then be {7:3, 8:8, 9:5, 10:2}
    # These global frequencies are not all possible, for example, if the total amount of mines was 9, then the 2 combinations with 10 mines would not be valid, this is accounted for later in determine_probabilities
    def determine_global_freq(self):
        global_freq = {}

        # This block determines, based on the lists in i[2] of the sublists, the frequencies of the possible global mine counts
        for i in self.islands:

            helper = {}
            island_freq = {}

            # Checks the frequencies of the legnths of lists in the possible combos for each sublist of islands
            for j in i[2]:
                if len(j) in island_freq:
                    island_freq[len(j)] += 1
                else:
                    island_freq[len(j)] = 1

            # Uses the frequencies of the lengths of lists in each sublist of islands to create a global frequency of lengths
            for j in island_freq:
                if not global_freq:
                    global_freq = island_freq
                    break
                else:
                    for k in global_freq:
                        if j+k in helper:
                            helper[j+k] += island_freq[j]*global_freq[k]
                        else:
                            helper[j+k] = island_freq[j]*global_freq[k]


            if helper:
                global_freq = helper.copy()

        return global_freq


    # Determines for each island, what the probability of there being a mine is, in each non-clicked tile in the island
    def determine_probabilities(self):

        # Determines what the global frequencies of mine combinations is
        global_freq = self.determine_global_freq()

        # Determines what the island-level frequencies of mine combinations is
        for i in self.islands:
            island_freq = {}

            for j in i[2]:
                if len(j) in island_freq:
                    island_freq[len(j)] += 1
                else:
                    island_freq[len(j)] = 1

            total_combinations = 0
            possible_mines = {}

            # Gets the global frequency if the current island in the iteration didn't exist
            glob_one = self.get_glob_one(global_freq.copy(), island_freq)

            # For each possible mine combination in the island's third element, determines how many global combinations there are where that island-level possible combination is true
            for j in i[2]:
                for a in glob_one:
                    total_mines_left = self.num_mines - (len(j) + len(self.known_mines)+a)
                    total_tiles_left = self.tiles - len(self.tiles_with_data) 
                    partial_combinations = 0
                    if total_mines_left >= 0 and total_tiles_left >= 0 and total_tiles_left >= total_mines_left: 
                        partial_combinations = glob_one[a]*factorial(total_tiles_left)/(factorial(total_tiles_left-total_mines_left)*factorial(total_mines_left))
                        total_combinations += partial_combinations

                    for k in j:
                        if partial_combinations > 0:
                            if k in possible_mines:
                                possible_mines[k] += partial_combinations
                            else:
                                possible_mines[k] = partial_combinations

            # Determines the probability of there being a mine under a tile by taking the number of possible combos where that tile is a mine, divided by the total number of possible combos
            if total_combinations > 0:
                for k in possible_mines:
                    possible_mines[k] /= total_combinations


                # Assigns the calculated probabilities to the tile objects
                for j in i[1]:
                    self.board[j[0]][j[1]].has_some_data = True
                    if j in possible_mines.keys():
                        self.board[j[0]][j[1]].probability = possible_mines[j]
                        if self.board[j[0]][j[1]].probability == 1:
                            self.mine_known(j[0], j[1])
                    else:
                        self.tile_known(j[0], j[1])
