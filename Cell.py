class Cell:

    def __init__(self, status):
        self.is_mine = status
        self.uncovered = False
        self.mines_around = 0
        self.flagged = False
        self.probability = None
        self.has_some_data = False

    def prob_str(self):
        if not self.uncovered:
            if self.flagged:
                return "[ F ]"
            
            elif self.has_some_data:
                if self.probability == 1:
                    return "[ M ]"
                elif self.probability == 0:
                    return "[00%]"
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
