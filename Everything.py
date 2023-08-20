from math import factorial
import random
import tkinter as tk
from tkinter import ttk
from math import factorial

class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")

        self.board = None
        self.buttons = []
        self.flag_mode = False

        self.create_widgets()

    def create_widgets(self):
        self.info_label = tk.Label(self.root, text="Minesweeper Game")
        self.info_label.pack()

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack()

        self.flag_mode_button = ttk.Button(self.root, text="Flag Mode", command=self.toggle_flag_mode)
        self.flag_mode_button.pack()

        self.restart_button = ttk.Button(self.root, text="Restart Game", command=self.restart_game)
        self.restart_button.pack()

        self.start_game()

    def start_game(self):
        self.clear_board()
        self.board = Board(self.height_var.get(), self.width_var.get(), self.mines_var.get())
        self.update_board()

    def clear_board(self):
        for row in self.buttons:
            for button in row:
                button.destroy()
        self.buttons.clear()

    def update_board(self):
        for row in range(self.board.height):
            row_buttons = []
            for col in range(self.board.width):
                button = ttk.Button(self.grid_frame, text="", command=lambda r=row, c=col: self.click_tile(r, c))
                button.grid(row=row, column=col, padx=2, pady=2)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def click_tile(self, row, col):
        tile = self.board.board[row][col]
        if self.flag_mode:
            tile.flagged = not tile.flagged
            self.update_board()
        elif not tile.uncovered and not tile.flagged:
            outcome = self.board.tile_clicked(row, col)
            if outcome == False:
                self.update_board()
                self.end_game()
            else:
                self.update_board()

    def toggle_flag_mode(self):
        self.flag_mode = not self.flag_mode
        mode_text = "Flag Mode" if self.flag_mode else "Uncover Mode"
        self.flag_mode_button.config(text=mode_text)

    def end_game(self):
        self.update_board()
        decide_outcome(self.board)

    def restart_game(self):
        self.start_game()

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
        

def decide_outcome(finished_board):
    # Reveals the true values of all the mines
    for i in range(finished_board.height):
        for j in range(finished_board.width):
            if not finished_board.board[i][j].uncovered and finished_board.board[i][j].is_mine:
                finished_board.board[i][j].uncovered = True
    finished_board.probabilities = False
    print(finished_board)

    # Determines whether you won or lost
    if len(finished_board.checked_tiles) == finished_board.tiles - finished_board.num_mines:
        print("CONGRATULATIONS!!! YOU WON!!")
    else:
        print("You lost")

class Cell:
    def __init__(self, status):
        self.is_mine = status
        self.uncovered = False
        self.mines_around = 0
        self.flagged = False
        self.probability = 0
        self.has_some_data = False
        self.surrounding_tiles = set()
        self.known_tiles = set()
        self.cell_known_mines = 0

    def prob_str(self):
        if not self.uncovered:
            if self.flagged:
                return "[ F ]"
            
            elif self.has_some_data:
                if self.probability == 1:
                    return "[ M ]"
                elif self.probability == 0:
                    return "[00%]"
                elif 0 < self.probability < .095:
                    return f"[0{int(round(self.probability, 2)*100)}%]"
                else:
                    return f"[{int(round(self.probability, 2)*100)}%]"
                
            else:
                return "[   ]"
        else:
            if self.is_mine:
                return "[ M ]"
            else:
                return (f'[ {self.mines_around} ]')

    def no_prob_str(self):
        if not self.uncovered:
            if self.flagged:
                return "[ F ]"

            else:
                return "[   ]"
        else:
            if self.is_mine:
                return "[ M ]"
            else:
                return (f'[ {self.mines_around} ]')

def product(args):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = [tuple(pool) for pool in args]
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def random_sample_with_exclusion(start_range, end_range, exclude_num, sample_size):
    # Create a list of numbers within the specified range, excluding the excluded number
    numbers = [num for num in range(start_range, end_range+1) if num != exclude_num]

    # Randomly sample without replacement from the numbers list
    random_sample = [-1] + quickSort(random.sample(numbers, sample_size))
    return random_sample

def partition(aList, first, last):
    pivotValue = aList[first]

    left_mark = first+1
    right_mark = last

    done = False
    while not done:
        while left_mark <= right_mark and aList[left_mark] >= pivotValue:
            left_mark += 1

        while right_mark >= left_mark and aList[right_mark] <= pivotValue:
            right_mark -= 1

        if right_mark < left_mark:
            done = True
        else:
            temp = aList[left_mark]
            aList[left_mark] = aList[right_mark]
            aList[right_mark] = temp

    temp = aList[first]
    aList[first] = aList[right_mark]
    aList[right_mark] = temp

    return right_mark

def quickSortHelper(aList, first, last):
    if first < last:
        splitpoint = partition(aList, first, last)

        quickSortHelper(aList, first, splitpoint-1)
        quickSortHelper(aList, splitpoint+1, last)


def quickSort(aList):
    quickSortHelper(aList, 0, len(aList)-1)
    return aList

def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield list(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield list(pool[i] for i in indices)

if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()