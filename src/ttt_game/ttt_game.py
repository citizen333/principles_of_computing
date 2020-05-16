"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
# import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1  # Number of trials to run
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0  # Score for squares played by the other player


# Add your functions here.
def mc_trial(board, player):
    """
    Plays ttt game with random moves until someone wins or until draw
    :param board: provided.TTTBoard object
    :param player: PLAYERX or PLAYERO constant
    :return: None
    """
    while len(board.get_empty_squares()) > 0:
        random_row, random_col = random.choice(board.get_empty_squares())
        board.move(random_row, random_col, player)
        if board.check_win() is not None:
            return
        player = provided.switch_player(player)


# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
