import pytest

from poc.fifteen_puzzle import fp_game

@pytest.fixture
def half_messed_grid():
    grid_height = 4
    grid_width = 4
    shuffled_range = [8, 5, 1, 7, 6, 9, 2, 4, 3, 0, 10, 11, 12, 13, 14, 15]
    new_grid = list()
    for separator in range(0, grid_height * grid_width, grid_width):
        new_grid.append(shuffled_range[separator:separator + grid_width])
    print(new_grid)
    return fp_game.Puzzle(grid_height, grid_width, new_grid)

def test_lower_row_invariant(target_row = 2, target_col = 1):
    my_grid = fp_game.Puzzle(2, 2, initial_grid=[[0, 1], [2, 3]])
    print(my_grid)
    assert my_grid.get_height() == 2
    assert half_messed_grid.lower_row_invariant(target_row, target_col)
