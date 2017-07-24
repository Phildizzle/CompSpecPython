"""
Clone of 2048 game.
"""

import poc_2048_gui
import random as rnd

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    #input list must not be changed
    line = list(line)
    results = len(line)
    
    # Slide tiles to the front
    while 0 in line:
        line.remove(0)
    
    for dummy_tile in range(len(line) - 1):
        if line[dummy_tile] == line[dummy_tile + 1]:
            line[dummy_tile] *= 2
            del line[dummy_tile + 1]
            line.insert(dummy_tile + 1, 0)
        # find the end of "line"
        if dummy_tile + 2 > len(line):
            break
    # fill "line" up with zeros and slide to front
    while 0 in line:
        line.remove(0)
    while len(line) != results:
        line.append(0)
    
    
    return line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self._cells = []
        self._initial = {UP: [(0, dummy_col) for dummy_col in range(self._width)],
                        DOWN: [(self._height - 1, dummy_col) for dummy_col in range(self._width)],
                        LEFT: [(dummy_row, 0) for dummy_row in range(self._height)],
                        RIGHT: [(dummy_row, self._width - 1) for dummy_row in range(self._height)]}
        self.reset()
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._cells = [[0 for dummy_col in range(self._width)] 
                      for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._cells)
#        nessage = ""
#        for i in range(len(self.grid)):
#            res += str(self._cells[i]) + "\n"

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        number = self._height
        change_dir = False
        if direction == LEFT or direction == RIGHT:
            number = self._width
        for dummy_i in self._initial[direction]:
            cuts = self.cut(dummy_i, OFFSETS[direction], number)
            merges = merge(cuts)
            if cuts != merges:
                change_dir = True
            self.modify(dummy_i, OFFSETS[direction], number, merges)
        if change_dir:
            self.new_tile()
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        helper = True
        col = 0
        row = 0
        while helper:
            col = rnd.randrange(self._width)
            row = rnd.randrange(self._height)
            if self._cells[row][col] == 0:
                helper = False
        if rnd.random() <= .1:
            self._cells[row][col] = 4
        else:
            self._cells[row][col] = 2

    def cut(self, start, direction, number):
        """
        Helper function to create lists for the move function.
        """
        results = []
        for dummy_i in range(number):
            row = start[0] + dummy_i * direction[0]
            col = start[1] + dummy_i * direction[1]
            results.append(self._cells[row][col])
        return results
    
    def modify(self, begin, direction, number, merges):
        """
        Another helper function to for the move function
        """
        for dummy_i in range(number):
            row = begin[0] + dummy_i * direction[0]
            col = begin[1] + dummy_i * direction[1]
            self._cells[row][col] = merges[dummy_i]
    
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._cells[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
