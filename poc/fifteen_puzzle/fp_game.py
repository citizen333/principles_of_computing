"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

# import poc_fifteen_gui

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
        Generate string representaion for puzzle
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
        try:
            # Check that zero is in correct position
            zero_row, zero_col = self.current_position(0, 0)
            assert zero_row == target_row
            assert zero_col == target_col
            # Check that cells of underlying rows are in correct position
            for row in range(target_row + 1, self._height):
                for col in range(self._width):
                    current_row, current_col = self.current_position(row, col)
                    assert current_row == row
                    assert current_col == col
            # Check that cells of current row is in correct position
            for col in range(target_col + 1, self._width):
                current_row, current_col = self.current_position(target_row, col)
                assert current_row == target_row
                assert current_col == col
            return True
        except AssertionError:
            return False

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)

        move_delta = ""
        move_string = ""
        zero_row, zero_col = self.current_position(0, 0)
        current_row, current_col = self.current_position(target_row, target_col)

        while (current_row, current_col) != (target_row, target_col):
            if (current_col == target_col) & ((target_row - current_row) == 1):
                move_delta = "uld"
            if zero_row > current_row:
                move_delta = "u"
            elif zero_col > current_col:
                move_delta = "l"
            elif (current_col - zero_col) > 1:
                move_delta = "r"
            elif zero_row < current_row:
                move_delta = "ld"
            elif current_row == target_row:
                move_delta = "urrdl"
            elif current_col < target_col:
                move_delta = "drrul"
            elif (current_col > target_col) & ((target_row - current_row) == 1):
                move_delta = "rulld"
            elif current_col > target_col:
                move_delta = "rdllu"
            elif current_col == target_col:
                move_delta = "druld"
            move_string += move_delta
            self.update_puzzle(move_delta)
            zero_row, zero_col = self.current_position(0, 0)
            current_row, current_col =\
                self.current_position(target_row, target_col)
        if zero_row == (target_row - 1):
                move_delta = "ld"
                move_string += move_delta
                self.update_puzzle(move_delta)
        assert self.lower_row_invariant(target_row, target_col - 1)
        return move_string



    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)

        move_delta = ""
        move_string = ""
        zero_row, zero_col = self.current_position(0, 0)
        current_row, current_col = self.current_position(target_row, 0)

        while (current_row, current_col) != (target_row, 0):
            if zero_row == target_row:
                move_delta = "ur"
            elif zero_row > current_row:
                move_delta = "u"
            elif zero_col > (current_col):
                move_delta = "l"
            elif (current_col - zero_col) > 1:
                move_delta = "r"
            elif zero_row < current_row:
                move_delta = "ld"
            elif self.current_position(target_row, 0) == (target_row - 1, 1):
                move_delta = "ruldrdlurdluurddlur"
            elif (current_col > 1) & ((target_row - current_row) == 1):
                move_delta = "rulld"
            elif current_col > 1:
                move_delta = "rdllu"
            elif current_col == 1:
                move_delta = "druld"
            move_string += move_delta
            self.update_puzzle(move_delta)
            zero_row, zero_col = self.current_position(0, 0)
            current_row, current_col = self.current_position(target_row, 0)
        
        move_delta = "r" * (self.get_width() - 2)
        move_string += move_delta
        self.update_puzzle(move_delta)

        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        try:
            zero_row, zero_col = self.current_position(0, 0)
            assert zero_row == 0
            assert zero_col == target_col
            # Check that cells of rows below 1 are in correct position
            for row in range(2, self._height):
                for col in range(self._width):
                    current_row, current_col = self.current_position(row, col)
                    assert current_row == row
                    assert current_col == col
            # Check that cells of row 0 and 1 are in correct position
            for row in range(2):
                for col in range(target_col, self._width):
                    if row == 0 and col == target_col:
                        continue
                    current_row, current_col = self.current_position(row, col)
                    assert current_row == row
                    assert current_col == col
            return True
        except AssertionError:
            return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        try:
            for col in range(target_col + 1, self._width):
                current_row, current_col = self.current_position(0, col)
                assert current_row == 0
                assert current_col == col
            assert self.lower_row_invariant(1, target_col)
            return True
        except AssertionError:
            return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        move_delta = ""
        move_string = ""
        zero_row, zero_col = self.current_position(0, 0)
        current_row, current_col = self.current_position(0, target_col)

        while (current_row, current_col) != (0, target_col):
            if zero_col == target_col:
                move_delta = "ld"
            elif zero_col > current_col:
                move_delta = "l"
            elif (target_col - current_col == 1) & (current_row == 0):
                move_delta = "uld"
            elif zero_row > current_row:
                move_delta = "urdl"
            elif current_col < (target_col - 1):
                move_delta = "urrdl"
            elif target_col - current_col == 1:
                move_delta = "urdlurrdluldrruld"
            move_string += move_delta
            self.update_puzzle(move_delta)
            current_row, current_col = self.current_position(0, target_col)
            zero_row, zero_col = self.current_position(0, 0)
        assert self.row1_invariant(target_col - 1)
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        move_string = self.solve_interior_tile(1, target_col)
        move_delta = "ur"
        move_string += move_delta
        self.update_puzzle(move_delta)
        assert self.row0_invariant(target_col)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        move_string = ""
        move_delta = "lu"
        move_string += move_delta
        self.update_puzzle(move_delta)
        
        while not self.lower_row_invariant(0, 0):
            move_delta = "rdlu"
            move_string += move_delta
            self.update_puzzle(move_delta)
        
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        zero_row, zero_col = self.current_position(0, 0)
        move_delta = ("r" * (self._width - zero_col - 1))\
                   + ("d" * (self._height - zero_row - 1))
        move_string += move_delta
        self.update_puzzle(move_delta)
        for row in range(self._height-1, 1, -1):
            for col in range(self._width-1, 0, -1):
                move_string += self.solve_interior_tile(row, col)
            move_string += self.solve_col0_tile(row)
        for col in range(self._width-1, 1, -1):
            move_string += self.solve_row1_tile(col)
            move_string += self.solve_row0_tile(col)
        move_string += self.solve_2x2()
        return move_string

# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))