"""
Clone of 2048 game.
"""
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    merged_line = [0] * len(line)

    target_idx = 0
    for entrance in line:
        if entrance > 0:
            if  merged_line[target_idx] == 0:
                merged_line[target_idx] = entrance
            elif merged_line[target_idx] == entrance:
                merged_line[target_idx] += entrance
                target_idx += 1
            else:
                target_idx += 1
                merged_line[target_idx] = entrance
    return merged_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._initial_tiles_of_directions = {
            UP: list(zip([0] * grid_width, range(grid_width))),
            DOWN: list(zip([grid_height - 1] * grid_width, range(grid_width))),
            LEFT: list(zip(range(grid_height), [0] * grid_height)),
            RIGHT: list(zip(range(grid_height), [grid_width - 1] * grid_height))
        }
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._board_grid = [[0] * self.get_grid_width() for row in range(self.get_grid_height())]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_str = str()
        for row in self._board_grid:
            grid_str += str(row) + '\n'

        return grid_str

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        moves = 0

        for row, col in self._initial_tiles_of_directions[direction]:
            move_cells = list()
            move_values = list()
            while 0 <= row < self.get_grid_height()\
                    and 0 <= col < self.get_grid_width():
                move_cells.append((row, col))
                row += OFFSETS[direction][0]
                col += OFFSETS[direction][1]
            # print(move_cells)

            for row, col in move_cells:
                move_values.append(self.get_tile(row, col))
            # print(move_values)

            merged_values = merge(move_values)
            # print(merged_values)

            if merged_values != move_values:
                moves += 1

            for tile, val in zip(move_cells, merged_values):
                self.set_tile(tile[0], tile[1], val)

        if moves > 0:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        index_of_zero = 0
        index_of_zero_list = []

        for row in self._board_grid:
            for elem in row:
                if elem == 0:
                    index_of_zero_list.append(index_of_zero)
                index_of_zero += 1

        if len(index_of_zero_list) > 0:
            rand_index = random.choice(index_of_zero_list)
            grid_row = rand_index // self.get_grid_width()
            grid_col = rand_index % self.get_grid_width()
            rand_number = random.choice([2] * 9 + [4])
            self._board_grid[grid_row][grid_col] = rand_number

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._board_grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._board_grid[row][col]

    def get_grid(self):
        """
        Return the whole grid
        """
        return self._board_grid