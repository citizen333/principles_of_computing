import pytest

from poc.fifteen_puzzle import fp_game

@pytest.mark.parametrize("grid, target_row, target_col",[
    ([[1, 1, 1, 1],
      [1, 1, 1, 1],
      [1, 1, 1, 1],
      [0, 13, 14, 15]], 3, 0),
    ([[1, 1, 1, 1],
      [1, 1, 1, 1],
      [1, 1, 1, 0],
      [12, 13, 14, 15]], 2, 3),
    ([[1, 1, 1, 1],
      [1, 1, 0, 7],
      [8, 9, 10, 11],
      [12, 13, 14, 15]], 1, 2)
])
def test_lower_row_invariant(grid, target_row, target_col):
    test_puzzle = fp_game.Puzzle(4, 4, grid)
    assert test_puzzle.lower_row_invariant(target_row, target_col)

@pytest.mark.parametrize("grid, target_row, target_col, move_string",[
    ([[1, 1, 1, 1],
      [1, 1, 1, 1],
      [1, 1, 1, 1],
      [14, 1, 0, 15]], 3, 2, "llurrdl"),
    ([[14, 1, 1, 1],
      [1, 1, 1, 1],
      [1, 1, 1, 1],
      [1, 1, 0, 15]], 3, 2, "uuulldrruldrulddrulddruld"),
    ([[1, 1, 14, 1],
      [1, 1, 1, 1],
      [1, 1, 1, 1],
      [1, 1, 0, 15]], 3, 2, "uuulddrulddruld"),
    ([[1, 1, 1, 1],
      [1, 1, 1, 1],
      [1, 1, 1, 13],
      [1, 0, 14, 15]], 3, 1, "urrulldrullddruld")
])
def test_solve_interior_tile(grid, target_row, target_col, move_string):
    test_puzzle = fp_game.Puzzle(4, 4, grid)
    assert test_puzzle.solve_interior_tile(target_row, target_col) ==\
        move_string

@pytest.mark.parametrize("grid, target_row, move_string",[
    ([[12, 1, 1, 1],
      [1, 1, 1, 1],
      [1, 1, 1, 1],
      [0, 13, 14, 15]], 3, "uruuldrulddruldruldrdlurdluurddlurrr"),
    ([[1, 1, 1, 1],
      [1, 1, 1, 12],
      [1, 1, 1, 1],
      [0, 13, 14, 15]], 3, "ururrdllurdlludruldruldrdlurdluurddlurrr"),
    ([[1, 1, 1, 1],
      [1, 1, 1, 1],
      [12, 1, 1, 1],
      [0, 13, 14, 15]], 3, "urrr"),
    ([[1, 1, 1, 1],
      [1, 1, 1, 1],
      [1, 1, 12, 1],
      [0, 13, 14, 15]], 3, "urrulldruldrdlurdluurddlurrr")
])
def test_solve_col0_tile(grid, target_row, move_string):
    test_puzzle = fp_game.Puzzle(4, 4, grid)
    assert test_puzzle.solve_col0_tile(target_row) == move_string
    
@pytest.mark.parametrize("grid, target_col",[
    ([[1, 1, 0, 3],
      [1, 1, 6, 7],
      [8, 9, 10, 11],
      [12, 13, 14, 15]], 2)
])
def test_row0_invariant(grid, target_col):
    test_puzzle = fp_game.Puzzle(4, 4, grid)
    assert test_puzzle.row0_invariant(target_col)

@pytest.mark.parametrize("grid, target_col",[
    ([[1, 1, 1, 3],
      [1, 1, 0, 7],
      [8, 9, 10, 11],
      [12, 13, 14, 15]], 2)
])
def test_row1_invariant(grid, target_col):
    test_puzzle = fp_game.Puzzle(4, 4, grid)
    assert test_puzzle.row1_invariant(target_col)
    
@pytest.mark.parametrize("grid, target_col, move_string",[
    ([[3, 1, 1, 0],
      [1, 1, 1, 7],
      [8, 9, 10, 11],
      [12, 13, 14, 15]], 3, "ldllurdlurrdlurdlurrdluldrruld"),
    ([[1, 1, 0, 3],
      [2, 1, 6, 7],
      [8, 9, 10, 11],
      [12, 13, 14, 15]], 2, "ldlurdlurrdluldrruld"),
    ([[1, 2, 0, 3],
      [1, 1, 6, 7],
      [8, 9, 10, 11],
      [12, 13, 14, 15]], 2, "ld")
])
def test_solve_row0_tile(grid, target_col, move_string):
    test_puzzle = fp_game.Puzzle(4, 4, grid)
    assert test_puzzle.solve_row0_tile(target_col) == move_string
    
@pytest.mark.parametrize("grid, move_string",[
    ([[5, 4, 2, 3],
      [1, 0, 6, 7],
      [8, 9, 10, 11],
      [12, 13, 14, 15]], "lurdlu"),
    ([[1, 5, 2, 3],
      [4, 0, 6, 7],
      [8, 9, 10, 11],
      [12, 13, 14, 15]], "lurdlurdlu"),
    ([[4, 1, 2, 3],
      [5, 0, 6, 7],
      [8, 9, 10, 11],
      [12, 13, 14, 15]], "lu")
])
def test_solve_2x2(grid,  move_string):
    test_puzzle = fp_game.Puzzle(4, 4, grid)
    assert test_puzzle.solve_2x2() == move_string

@pytest.mark.parametrize("grid, n_rows, n_cols, move_string",[
    ([[0, 1, 2, 3],
      [4, 5, 6, 7],
      [8, 9, 10, 11],
      [12, 13, 14, 15]], 4, 4,
     "rrrddduldulduldurrruldulduldurrruldurlduldurldlurdlurdlu"),
    ([[8, 7, 6],
      [5, 4, 3],
      [2, 1, 0]], 3, 3,
     "uulldrruldrulddrulduulddruldururdlludruldruldrdlurdluurddlurrlurldlurdlurdlurrdluldrruldlurdlu")
])
def test_solve_puzzle(grid, n_rows, n_cols, move_string):
    test_puzzle = fp_game.Puzzle(n_rows, n_cols, grid)
    assert test_puzzle.solve_puzzle() == move_string