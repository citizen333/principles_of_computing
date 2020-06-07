import pytest
import random

from poc.tic_tac_toe import ttt_game, poc_ttt_provided as provided

ttt_game.SCORE_CURRENT = 1.0
ttt_game.SCORE_OTHER = 2.0


@pytest.fixture
def empty_board():
    return provided.TTTBoard(3)

@pytest.fixture
def trialed_board(empty_board, trials_result):
    if trials_result == "EMPTY":
        return empty_board
    elif trials_result == "DRAW":
        random.seed(7)
        ttt_game.mc_trial(empty_board, provided.PLAYERO)
        return empty_board
    elif trials_result == "PLAYER_X":
        random.seed(1)
        ttt_game.mc_trial(empty_board, provided.PLAYERX)
        return empty_board
    elif trials_result == "PLAYER_O":
        random.seed(11)
        ttt_game.mc_trial(empty_board, provided.PLAYERO)
        return empty_board

@pytest.fixture
def scores_board(empty_board, scores_result):
    if scores_result == "ZERO":
        return [[0] * empty_board.get_dim()
                for dummy_row in range(empty_board.get_dim())]
    elif scores_result == "RANDOM":
        random.seed(11)
        random_grid = list()
        for row in range(empty_board.get_dim()):
            random_row = list()
            for col in range(empty_board.get_dim()):
                random_row.append(random.randrange(-9, 10))
            random_grid.append(random_row)
        return random_grid

"""
Test mc_trial function
"""


@pytest.mark.parametrize("player, seed, game_result", [
    (provided.PLAYERX, 1, 2),
    (provided.PLAYERX, 3, 3),
    (provided.PLAYERX, 7, 4),
    (provided.PLAYERO, 10, 2),
    (provided.PLAYERO, 11, 3),
    (provided.PLAYERO, 7, 4)
])
def test_mc_trial(empty_board, player, seed, game_result):
    random.seed(seed)
    ttt_game.mc_trial(empty_board, player)
    assert empty_board.check_win() == game_result


"""
Test mc_update_scores function
"""


@pytest.mark.parametrize("trials_result, player, scores_result, score_board_result", [
    ("EMPTY", provided.PLAYERX, "ZERO", [[0, 0, 0],
                                         [0, 0, 0],
                                         [0, 0, 0]]
     ),
    ("DRAW", provided.PLAYERO, "RANDOM", [[5, 8, 5],
                                          [5, 7, 9],
                                          [-3, -4, 7]]
     ),
    ("PLAYER_X", provided.PLAYERX, "ZERO", [[-2.0, -2.0, 1.0],
                                            [1.0, 1.0, 1.0],
                                            [-2.0, 1.0, -2.0]]
     ),
    ("PLAYER_X", provided.PLAYERO, "ZERO", [[-1.0, -1.0, 2.0],
                                            [2.0, 2.0, 2.0],
                                            [-1.0, 2.0, -1.0]]
     ),
    ("PLAYER_O", provided.PLAYERX, "RANDOM", [[7.0, 7.0, 5],
                                              [7.0, 7, 8.0],
                                              [-1.0, -2.0, 6.0]]
     ),
    ("PLAYER_O", provided.PLAYERO, "RANDOM", [[6.0, 6.0, 5],
                                              [6.0, 7, 7.0],
                                              [-2.0, -3.0, 5.0]]
     )
])
def test_mc_update_scores(trialed_board, player, scores_board, score_board_result):
    ttt_game.mc_update_scores(scores_board, trialed_board, player)
    assert scores_board == score_board_result
