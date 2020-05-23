import pytest
import random

from twenty_forty_eight.game_2048 import *

@pytest.fixture
def initial_grid():
    random.seed(100)
    return TwentyFortyEight(7, 5)

@pytest.fixture
def tiled_grid(initial_grid):
    random.seed(110)
    initial_grid.new_tile()
    random.seed(120)
    initial_grid.new_tile()
    return initial_grid


"""
Test merge handler for 2048 game
"""

@pytest.mark.parametrize("input_list, merged_list",[
                             (
                                [2, 0, 2, 4], [4, 4, 0, 0]
                             ),
                             (
                                [0, 0, 2, 2], [4, 0, 0, 0]
                             ),
                             (
                                [2, 2, 0, 0], [4, 0, 0, 0]
                             ),
                             (
                                [2, 2, 2, 2, 2], [4, 4, 2, 0, 0]
                             ),
                             (
                                [8, 16, 16, 8], [8, 32, 8, 0]
                             )
                         ])
def test_merge(input_list, merged_list):
    assert merge(input_list) == merged_list


"""
Test grid creation for 2048 game
"""

@pytest.mark.parametrize("grid_height, grid_width, seed, output",[
    (
        10, 1, 1, [[0], [2], [4], [0], [0], [0], [0], [0], [0], [0]]
    ),
    (
        4, 4, 3, [[0, 0, 0, 0], [0, 0, 0, 4], [0, 2, 0, 0], [0, 0, 0, 0]]
    ),
    (
        2, 8, 7, [[0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 2, 0, 0, 0, 0, 0]]
    )
])
def test_grid_creation(grid_height, grid_width, seed, output):
    random.seed(seed)
    test_game = TwentyFortyEight(grid_height, grid_width)
    assert test_game.get_grid() == output

def test_string_representation_of_grid(initial_grid):
    output = '[0, 0, 0, 0, 0]\n' \
             '[0, 0, 0, 0, 2]\n' \
             '[0, 0, 0, 0, 0]\n' \
             '[0, 0, 0, 0, 0]\n' \
             '[0, 0, 0, 0, 0]\n' \
             '[0, 0, 0, 0, 0]\n' \
             '[2, 0, 0, 0, 0]\n'
    assert str(initial_grid) == output

def test_hight_getter(initial_grid):
    assert initial_grid.get_grid_height() == 7

def test_width_getter(initial_grid):
    assert initial_grid.get_grid_width() == 5

@pytest.mark.parametrize("seed, output",[
    (
        20, [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 2],
             [2, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 2, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [2, 0, 0, 0, 0]]
    ),
    (
        30, [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 2],
             [0, 0, 0, 0, 0],
             [2, 0, 0, 0, 4],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [2, 0, 0, 0, 0]]
    ),
    (
        40, [[2, 0, 0, 0, 0],
             [0, 0, 0, 0, 2],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [2, 4, 0, 0, 0]]
    )
])
def test_adding_random_tiles_to_grid(initial_grid, seed, output):
    random.seed(seed)
    initial_grid.new_tile()
    random.seed(seed**2)
    initial_grid.new_tile()
    assert initial_grid.get_grid() == output

def test_reset_grid(tiled_grid, seed = 50):
    random.seed(seed)
    tiled_grid.reset()
    output = [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 2, 0],
              [0, 0, 0, 0, 0],
              [0, 2, 0, 0, 0]]
    assert tiled_grid.get_grid() == output

@pytest.mark.parametrize("row, col", [
    (
        0, 2
    ),
    (
        1, 3
    ),
    (
        6, 0
    )
])
def test_getting_tile(initial_grid, row, col):
    assert initial_grid.get_tile(row, col) == initial_grid._board_grid[row][col]

@pytest.mark.parametrize("row, col, value", [
    (
        0, 2, 4
    ),
    (
        1, 3, 0
    ),
    (
        6, 0, 2048
    )
])
def test_setting_tile(initial_grid, row, col, value):
    initial_grid.set_tile(row, col, value)
    assert initial_grid.get_tile(row, col) == value