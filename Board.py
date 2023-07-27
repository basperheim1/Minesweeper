import random
from QuickSort import quickSort
from itertools import combinations
from Cell import Cell
from Product import product
from math import factorial


class Board:
    def __init__(self, height, width, num_mines):
        self.height = height
        self.width = width
        self.num_mines = num_mines
        self.tiles = height * width
        self.mine_locations = quickSort(random.sample(range(0, self.tiles), self.num_mines))
        print(self.mine_locations)
        self.mine_locations.insert(0, -1)
        self.board = []
        self.unknown_neighbors = {}
        self.tiles_with_data = set()
        self.uncovered_tiles = 0
        self.need_to_check = []
        self.probabilities = False
        for i in range(height):
            self.board.append([])
            for j in range(width):
                if i*width+j == self.mine_locations[-1]:
                    self.board[i].append(Cell(True))
                    self.mine_locations.pop()
                else:
                    self.board[i].append(Cell(False))

    # Overrides the print method, so it prints the board when called
    def __str__(self):
        if self.probabilities:
            formatted_string = '\n'.join([' '.join(map(Cell.prob_str, sublist)) for sublist in self.board])
        else:
            formatted_string = '\n'.join([' '.join(map(Cell.no_prob_str, sublist)) for sublist in self.board])

        return formatted_string

    # Executes if a tile pressed is not a mine
    def check_surrounding_mines(self, row, column):
        # Creates a dict with the pressed tile as a key, and adds the covered surrounding tiles to the value list
        need_to_check = {(row, column):[]}

        # Uncovers the tile on the outputted board
        self.board[row][column].uncovered = True

        # Adds the tile that was pressed to the dictionary of uncovered tiles
        self.unknown_neighbors[(row, column)] = []
        total_mines = 0

        # Goes through the 8 tiles around the pressed tile
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Tries to remove the pressed tile from the surrounding tiles' list
                try:
                    self.unknown_neighbors[(row + i, column + j)].remove((row, column))
                except KeyError:
                    pass
                except ValueError:
                    pass
                # Checks how many mines are around the pressed tile
                if 0 <= row+i < self.height and 0 <= column+j < self.width:
                    self.tiles_with_data.add((row+i, column+j))
                    self.board[row+i][column+j].has_some_data = True
                    if self.board[row+i][column+j].is_mine:
                        total_mines += 1
                    # If a surrounding tile is covered, adds it to the pressed tile's list
                    if not self.board[row+i][column+j].uncovered:
                        need_to_check[(row, column)].append((row + i, column + j))
                        self.unknown_neighbors[(row, column)].append((row + i, column + j))

        # Sets pressed tile's mines_around to the total amount of mines around
        self.board[row][column].mines_around = total_mines
        if total_mines == 0:
            for i in need_to_check[(row, column)]:
                if not self.board[i[0]][i[1]].uncovered:
                    self.tile_clicked(i[0], i[1])

    # Method executes if a tile is clicked
    def tile_clicked(self, row, column):
        # Adds to the uncoverd_tiles counter
        self.uncovered_tiles += 1
        # If cell is a mine, returns false, else calls other method and then returns True
        if self.board[row][column].is_mine:
            self.board[row][column].uncovered = True
            return False
        else:
            self.check_surrounding_mines(row, column)
            return True
        
    def check_combination(self, combination):
        if len(combination) > self.num_mines:
            return False
        for i in self.unknown_neighbors:
            if sum([1 for j in self.unknown_neighbors[i] if j in combination]) != self.board[i[0]][i[1]].mines_around:
                return
        return True

        

    def determine_combos(self):
        uncovered_tiles_with_combos = {}
        for i in self.unknown_neighbors:
            if len(self.unknown_neighbors[i]) > 0:
                uncovered_tiles_with_combos[i] = list(combinations(self.unknown_neighbors[i], self.board[i[0]][i[1]].mines_around))

        '''
        uncovered_tiles_with_combos is a dictionary with the keys being all uncovered tiles with more than 0 mines around it, and the 
        value being a tuple of tuples, with each sub-tuple being a possible combination of mines around that uncovered tile

        '''
        uncovered_tiles_strictly_combos = [uncovered_tiles_with_combos[i] for i in uncovered_tiles_with_combos]

        '''
        uncovered_tiles_strictly_combos is a list with the elements being the value of the keys in the dictionary
        '''

        total_possible_combo = list(product(uncovered_tiles_strictly_combos))
    
        possible_combos_w_duplicates = []
        for i in total_possible_combo:
            possible_combos_w_duplicates.append([])
            for j in i:
                for k in j:
                    possible_combos_w_duplicates[-1].append(k)

        possible_combos = set()
        for i in possible_combos_w_duplicates:
            possible_combos.add(tuple(set(i)))
        
        correct_combinations = set()
        for i in possible_combos:
            if self.check_combination(i):
                correct_combinations.add(i)
        return correct_combinations
    

    def check_probabilities(self, correct_combinations):
        total_combinations = 0
        possible_mines = {}
        for i in correct_combinations:
            total_mines_left = self.num_mines - len(i)
            total_tiles_left = self.tiles - len(self.tiles_with_data)
            partial_combinations = factorial(total_tiles_left)/(factorial(total_tiles_left-total_mines_left)*factorial(total_mines_left))
            total_combinations += partial_combinations
            for j in i:
                if j in possible_mines:
                    possible_mines[j] += partial_combinations
                else:
                    possible_mines[j] = partial_combinations

        for k in possible_mines:
            possible_mines[k] = possible_mines[k] / total_combinations

        for i in self.tiles_with_data:
            if i not in possible_mines:
                self.board[i[0]][i[1]].probability = 0
            else:
                self.board[i[0]][i[1]].probability = possible_mines[i]

        return possible_mines