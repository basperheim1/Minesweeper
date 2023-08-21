class Tile:

    # Initializes the tile, creates various attributes used in determining the probability of the tile being a mine
    def __init__(self, status):
        self.is_mine = status
        self.uncovered = False
        self.flagged = False
        self.has_some_data = False
        self.mines_around = 0
        self.probability = 0
        self.tile_known_mines = 0
        self.surrounding_tiles = set()
        self.known_tiles = set()

    # Determines, based on the tile's state, what to return as a string 
    # This method deals only when probabilities are requested to be on screen
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
            
    # Determines, based on the tile's state, what to return as a string 
    # This method deals only when probabilities are NOT requested to be on screen
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
