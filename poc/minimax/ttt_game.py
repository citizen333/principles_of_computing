"""
Mini-max Tic-Tac-Toe Player
"""

# import poc_ttt_gui
from poc.tic_tac_toe import poc_ttt_provided as provided

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    scores_dict = {}
    if board.check_win() is not None:
        return SCORES[board.check_win()], (-1, -1)
    else:
        for move in board.get_empty_squares():
            clone_board = board.clone()
            clone_board.move(move[0], move[1], player)
            score = mm_move(clone_board, provided.switch_player(player))[0]
            if score * SCORES[player] == 1:
                return score, move
            else:
                scores_dict[move] = score * SCORES[player]
        max_score = max(scores_dict.values())
        minimax_moves = [key for key, val in scores_dict.items()
                             if val == max_score]
        return max_score * SCORES[player], minimax_moves[0]

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)