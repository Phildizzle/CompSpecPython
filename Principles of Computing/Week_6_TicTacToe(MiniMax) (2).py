"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

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
    winner = board.check_win()
    move = ()
    score = 0
    empty_board = board.get_empty_squares()
    best_move = ()
    if winner != None:
        if winner == provided.PLAYERX:
            score = SCORES[provided.PLAYERX]
        if winner == provided.PLAYERO:
            score = SCORES[provided.PLAYERO]
        if winner == provided.DRAW:
            score = 0
        move = (-1, -1)
        return score, move

    if player == provided.PLAYERX:
        best_score = -1
        for tile in empty_board:
            board_clone = board.clone()
            board_clone.move(tile[0], tile[1], player)
            pot_move = (tile[0], tile[1])
            score, move = mm_move(board_clone, provided.PLAYERO)
            if score > best_score:   
                best_score = score
                best_move = pot_move
            if score == SCORES[player]:  
                return score, pot_move
        return best_score, best_move
    elif player == provided.PLAYERO:
        best_score = 1
        for tile in empty_board:
            board_clone = board.clone()
            board_clone.move(tile[0], tile[1], player)
            pot_move = (tile[0], tile[1])
            score, move = mm_move(board_clone, provided.PLAYERX)
            if score < best_score:
                best_score = score
                best_move = pot_move
            if score == SCORES[player]:
                return score, pot_move
        return best_score, best_move

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
EMPTY = 1
PLAYERX = 2
PLAYERO = 3

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)