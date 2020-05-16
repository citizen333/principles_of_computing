import pytest
import random

from ttt_game import ttt_game
from ttt_game import poc_ttt_provided as provided

@pytest.fixture
def empty_board():
    return provided.TTTBoard(5)

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
def tes_mc_trial(empty_board, player, seed, game_result):
    random.seed(seed)
    ttt_game.mc_trial(empty_board, player)
    assert empty_board.check_win() == game_result