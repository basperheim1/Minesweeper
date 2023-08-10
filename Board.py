import random
from Cell import Cell
from RandomFunctions import random_sample_with_exclusion, combinations
from math import factorial

class Board:
    def __init__(self, height, width, num_mines, first_row, first_column):
        self.mines = set()
        self.height = height
        self.width = width
        self.num_mines = num_mines
        self.tiles = height * width
        self.probabilities = False
        self.tiles_with_data = set()
        self.checked_tiles = set()
        self.known_tiles = set()
        self.mine_locations = random_sample_with_exclusion(0, self.tiles-1, first_row*width+first_column, num_mines)
        self.possible_combos = []
        # print(self.mine_locations[1:])
        self.known_mines = 0
        self.board = []
        for i in range(height):
            self.board.append([])
            for j in range(width):
                if i*width+j == self.mine_locations[-1]:
                    self.board[i].append(Cell(True))
                    self.mine_locations.pop()
                else:
                    self.board[i].append(Cell(False))


        for i in range(height):
            for j in range(width):
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if 0 <= i + k < self.height and 0 <= j + l < self.width and not k == l == 0:
                            self.board[i][j].surrounding_tiles.add((i+k, j+l))
                            if self.board[i+k][j+l].is_mine:
                                self.board[i][j].mines_around += 1
                        
        self.tile_clicked(first_row, first_column)

    def mine_known(self, row, column):
        self.known_mines += 1
        self.mines.add((row, column))
        for i in self.board[row][column].surrounding_tiles:
            self.board[i[0]][i[1]].known_tiles.add((row, column))
            self.board[i[0]][i[1]].cell_known_mines += 1
        for i in self.possible_combos:
            try:
                i.remove((row, column))
            except:
                pass


    def tile_known(self, row, column):
        for i in self.board[row][column].surrounding_tiles:
            self.board[i[0]][i[1]].known_tiles.add((row, column))
        for i in self.possible_combos:
            try:
                i.remove((row, column))
            except:
                pass

    def __str__(self):
        if self.probabilities:
            formatted_string = '\n'.join([' '.join(map(Cell.prob_str, sublist)) for sublist in self.board])
        else:
            formatted_string = '\n'.join([' '.join(map(Cell.no_prob_str, sublist)) for sublist in self.board])

        return formatted_string


    def tile_clicked(self, row, column):
        if self.board[row][column].uncovered:
            pass
        else:
            self.tile_known(row, column)
            self.tiles_with_data.add((row, column))
            self.tiles_with_data.update(self.board[row][column].surrounding_tiles)
            self.checked_tiles.add((row, column))
            self.known_tiles.add((row, column))
            if self.board[row][column].is_mine:
                return False
            else:
                self.check_surrounding(row, column)
                return True

    def check_surrounding(self, row, column):
        self.board[row][column].uncovered = True
        self.determine_combos(row, column)
        if self.board[row][column].mines_around == 0:
            for i in self.board[row][column].surrounding_tiles:
                self.tile_clicked(i[0], i[1])

    def determine_combos(self, row, column):
        if self.board[row][column].mines_around != 0:
            thingy = list(combinations(self.board[row][column].surrounding_tiles.difference(self.board[row][column].known_tiles), self.board[row][column].mines_around-self.board[row][column].cell_known_mines))
            if self.possible_combos == []:
                self.possible_combos = thingy
            else:
                self.possible_combos = [set(x+y) for x in self.possible_combos for y in thingy]
                self.possible_combos = set(map(frozenset, self.possible_combos))
                self.possible_combos = [list(s) for s in self.possible_combos]
            self.possible_combos[:] = [combo for combo in self.possible_combos if self.check_combination(combo)]


    def check_combination(self, combo):
        if self.num_mines - (len(combo) + self.known_mines) > self.tiles - len(self.tiles_with_data):
            return False
        if len(combo) + self.known_mines > self.num_mines:
            return False
        for i in self.checked_tiles:
            if sum([1 for j in self.board[i[0]][i[1]].surrounding_tiles.difference(self.board[i[0]][i[1]].known_tiles) if j in combo]) != self.board[i[0]][i[1]].mines_around - self.board[i[0]][i[1]].cell_known_mines:
                return False
        return True

    def check_probabilities(self):
        total_combinations = 0
        possible_mines = {}
        for i in self.possible_combos:
            total_mines_left = self.num_mines - (len(i) + self.known_mines)
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
        
