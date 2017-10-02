"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representation for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        
        if self.get_number(target_row, target_col) != 0:
            return False
        for tile in range(target_col + 1, self._width):
            if self.current_position(target_row, tile) != (target_row, tile):
                return False
        for dummy_j in range(target_row + 1, self._height):
            for dummy_i in range(0, self._width):
                if self.current_position(dummy_j, dummy_i) != (dummy_j, dummy_i):
                    return False
        return True      
        
    def solve_interior_tile(self, target_row, target_col):
        """
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)
        row, col = self.current_position(target_row, target_col)
        # use move-helper function to get to target tile
        move_to_target = self.move_to_target(target_row, target_col, row, col)
        
        # update the grid
        self.update_puzzle(move_to_target)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_to_target
        
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # check if curr_pos (i, 0) where i > 1
        assert self.lower_row_invariant(target_row, 0)
        move = "ur"
        self.update_puzzle(move)
        row, col = self.current_position(target_row, 0)
        if row == target_row and col == 0:
            move_to_target = (self.get_width() - 2) * "r"
            self.update_puzzle(move_to_target)
            move += move_to_target
        else:
            move_to_target = self.move_to_target(target_row - 1, 1, row, col)
            # add solver move to str
            move_to_target += "ruldrdlurdluurddlu" + (self.get_width() - 1) * "r"
            self.update_puzzle(move_to_target)
            move += move_to_target
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
        return move


    def move_to_target(self, target_row, target_col, row, col):
        """
        Helper function. Moves tile to target position
        Target tile has to be above or to the left of target's future position.
        Returns move string.
        """
        move = ""
        # typical move to move target tile to target pos.
        solver_move = "druld"
        # move up first
        move = (target_row - row) * "u"
        # conditional statements for moving the tile:
        # 1. case curr_pos of tile and target_tile are in same col
        if (target_col - col) == 0:
            move += "ld" + ((target_row - row) - 1) * solver_move
        else:
            # 2. curr_pos of tile is on the left of target pos
            if (target_col - col) > 0:
                move += (target_col - col) * "l"
                if row == 0:
                    move += (abs(target_col - col) - 1) * "drrul"
                else:
                    move += (abs(target_col - col) - 1) * "urrdl"
            # 3. curr_pos of tile is on the right of target pos:
            elif (target_col - col) < 0:
                move += (abs(target_col - col) - 1) * "r"
                if row == 0:
                    move += abs(target_col - col) * "rdllu"
                else:
                    move += abs(target_col - col) * "rulld"
            move += (target_row - row) * solver_move
        return move
       
    
    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # asserts that curr_tile is in target_col
        if self.get_number(0, target_col) != 0:
            return False
        # asserts that tile (0,j) is solved, the grid below (0,j) and to the right is solved 
        for dummy_j in range(0, self.get_width()):
            for dummy_i in range(0, self.get_height()):
                if dummy_i > 1 or (dummy_i == 0 and dummy_j > target_col) or (dummy_i == 1 and dummy_j >= target_col):
                    if (dummy_i, dummy_j) != self.current_position(dummy_i, dummy_j):
                        return False
        return True
                        
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # assert that row 1 is solved
        if not self.lower_row_invariant(1, target_col):
            return False
        # asserts that tile proceeded to (1,j), the grid below (1,j) and to the right is solved
        for dummy_j in range(0, self.get_width()):
            for dummy_i in range(2, self.get_height()):
                if not (dummy_i, dummy_j) == self.current_position(dummy_i, dummy_j):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert  self.row0_invariant(target_col)
        move = "ld"
        self.update_puzzle(move)
        
        row, col = self.current_position(0, target_col)
        if row == 0 and col == target_col:
            return move
        else:
            move_to_target = self.move_to_target(1, target_col - 1, row, col)
            # 2x3 puzzle solver
            move_to_target += "urdlurrdluldrruld"
            self.update_puzzle(move_to_target)
            move += move_to_target
        return move

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        row, col = self.current_position(1, target_col)
        move = self.move_to_target(1, target_col, row, col)
        # for next move
        move += "ur"
        
        self.update_puzzle(move)
        return move

    ###########################################################
    # Phase 3 methods  
    
    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        pos_1_0 = self.get_number(1, 0)
        pos_0_0 = self.get_number(0, 0)
        pos_0_1 = self.get_number(0, 1)
        # create grid and solve individual cases
        grid = [pos_1_0, pos_0_0, pos_0_1]
        if grid == [self.get_width(), 1, self.get_width() + 1]:
            move = "ul"
        elif grid == [1, self.get_width() + 1, self.get_width()]:
            move =  "lurdlu"
        elif grid == [self.get_width() + 1, self.get_width(), 1]:
            move = "lu"
        self.update_puzzle(move)
        return move
    
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # initialize some values and start tile at bottom right corner
        col = self.get_width() - 1
        row = self.get_height() - 1
        move = ""
        curr_row, curr_col = self.current_position(0, 0)
        move_to_target = abs(curr_col - col) * "r" + abs(curr_row - row) * "d"
        self.update_puzzle(move_to_target)
        move += move_to_target

        #  apply solver methods
        for dummy_i in range(row, 1, -1):
            for dummy_j in range(col, 0, -1):
                move += self.solve_interior_tile(dummy_i, dummy_j)
            move += self.solve_col0_tile(dummy_i)
            
        for dummy_j in range(col, 1, -1):
            move += self.solve_row1_tile(dummy_j)
            move += self.solve_row0_tile(dummy_j)
            
        move += self.solve_2x2()
        return move

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))


