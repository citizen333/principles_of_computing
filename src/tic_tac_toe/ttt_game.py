"""
Monte Carlo Tic-Tac-Toe Player
"""

import random

# import poc_ttt_gui
import tic_tac_toe.poc_ttt_provided as provided

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


def mc_update_scores(scores, board, player):
    """
    Updates score board by increasing score in squares with winning moves and decreasing
    score in squares with losing moves
    :param scores: Grid of current scores. Will be updated after the function run
    :param board: Game board with results of trial
    :param player: PLAYERX or PLAYERO for whom the score is calculated
    :return: None
    """
    if board.check_win() == provided.DRAW or board.check_win() is None:
        return
    elif board.check_win() == player:
        player_coef = 1
    else:
        player_coef = -1

    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == provided.EMPTY:
                scores[row][col] += 0
            elif board.square(row, col) == player:
                scores[row][col] += player_coef * SCORE_CURRENT
            elif board.square(row, col) != player:
                scores[row][col] += -1 * player_coef * SCORE_OTHER


def get_best_move(board, scores):
    """
    Function to get the best next move. Works only if there are any free tiles left
    :param board: Game board with current state of the game
    :param scores: Grid of current scores. The next move will be to a free square with
    the highest score
    :return: If there are no free square left - None, else - (row,col) for the next move.
    """
    if len(board.get_empty_squares()) == 0:
        return

    max_val_squares = list()
    for row, col in board.get_empty_squares():
        new_score = scores[row][col]
        if len(max_val_squares) == 0:
            max_val_squares.append((row, col))
            current_max = float(new_score)
        elif new_score > current_max:
            max_val_squares = [tuple([row, col])]
            current_max = float(new_score)
        elif new_score == current_max:
            max_val_squares.append((row, col))
    print(board.get_empty_squares())
    print(scores)
    print(max_val_squares)
    return random.choice(max_val_squares)


def mc_move(board, player, trials):
    """
    Function to make the next move by simulating game several times and
    finding move with the highest score
    :param board: Game board with current state of the game
    :param player: PLAYERX or PLAYERO for the machine player
    :param trials: number of trials before making a move
    :return: If there are no free square left - None, else - (row,col) for the next move.
    """
    scores = [[0] * board.get_dim() for dummy_row in range(board.get_dim())]
    for dummy_trial in range(trials):
        trials_board = board.clone()
        mc_trial(trials_board, player)
        mc_update_scores(scores, trials_board, player)

    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
