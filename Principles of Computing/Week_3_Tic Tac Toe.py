"""
Monte Carlo Tic-Tac-Toe Player
- During this exercise I create a simple AI which learns specific moves by copying the player's 
  playstyle. 
- Runs best on Codeskulptor.org, since custom moduls are imported.
- Do not forget to comment out this block if you run the code in an IDE of your choice
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run; a value of "1" creates an "easy" opponent, 
# values from "5" create opponents more difficult to beat. More precisely, with more trials the opponent learns better.
SCORE_CURRENT = 1.0 # Score for squares played by the current player; increase this to make learning from losses more efficient.
SCORE_OTHER = 1.0   # Score for squares played by the other player; 
    
# Add your functions here.
def mc_trial(board, player):
    """ This function takes a current board and the next player to move. The function
    plays a game by starting with the given player making random moves, alternating
    between players. It returns when the game is over."""
    win = board.check_win()
    
    while win == None:
        empty_board = board.get_empty_squares()
        move = random.choice(empty_board)
        board.move(move[0], move[1], player)
        player = provided.switch_player(player)
        win = board.check_win()
    return
        
def winner_checker(winner, real_player):
    """
    Helper function for update scores.
    Returns 2 Boolean objects.
    """
    if real_player == winner:
        player_win = True
        other_win = False
        
    elif winner == provided.DRAW:
        player_win = False
        other_win = False
        
    else:
        other_win = True
        player_win = False
        
    return player_win, other_win    

def mc_update_scores(scores, board, player):
    """ This function scores the board and updates the scores' grid dependent on the game's outcome."""
    win = board.check_win()
    player_win, other_win = winner_checker(win, player)
    dim = board.get_dim()
    
    for dummy_row in range(dim):
        for dummy_col in range(dim):
            if player_win:
                if board.square(dummy_row, dummy_col) == player:
                    scores[dummy_row][dummy_col] += SCORE_CURRENT
                elif board.square(dummy_row, dummy_col) == provided.EMPTY:
                    scores[dummy_row][dummy_col] += 0
                else:
                    scores[dummy_row][dummy_col] -= SCORE_OTHER
            elif other_win:
                if board.square(dummy_row, dummy_col) == player:
                    scores[dummy_row][dummy_col] -= SCORE_CURRENT
                elif board.square(dummy_row, dummy_col) == provided.EMPTY:
                    scores[dummy_row][dummy_col] += 0
                else:
                    scores[dummy_row][dummy_col] += SCORE_OTHER
            elif win == provided.DRAW:
                scores[dummy_row][dummy_col] += 0
                    
def get_best_move(board, scores):
    """ Get best move of the board. If it's a draw, return a random move. 
    Returns a tuple with coordinates."""
    max_of_squares = []
    best_score = None
    tiles = board.get_empty_squares()
    
    for tile in tiles:
        if scores[tile[0]][tile[1]] >= best_score:
            best_score = scores[tile[0]][tile[1]]
    max_of_squares = [tile for tile in tiles if scores[tile[0]][tile[1]] == best_score]
    best_move = random.choice(max_of_squares)
    return best_move

def mc_move(board, player, trials):
    """ Uses Monte Carlo simulation to return a move for the machine player."""
    dim = board.get_dim()
    scores_total = [[0 for dummy_col in range(dim)] for dummy_row in range(dim)]
    
    for dummy_trial in range(trials):
        board_copy = board.clone() # clone-method from TTTBoard-Class
        mc_trial(board_copy, player)
        mc_update_scores(scores_total, board_copy, player)
        board_copy = board.clone() # clone-method from TTTBoard-Class
    ultimate_move = get_best_move(board_copy, scores_total)
    return ultimate_move


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you want to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

# Do not forget to comment out this block if you run the code in an IDE of your choice
#class TTTBoard:
#    """
#    Class to represent a Tic-Tac-Toe board.
#    """
#
#    def __init__(self, dim, reverse = False, board = None):
#        self._dim = dim
#        self._reverse = reverse
#        if board == None:
#            # Create empty board
#            self._board = [[EMPTY for dummycol in range(dim)] 
#                           for dummyrow in range(dim)]
#        else:
#            # Copy board grid
#            self._board = [[board[row][col] for col in range(dim)] 
#                           for row in range(dim)]
#            
#    def __str__(self):
#        """
#        Human readable representation of the board.
#        """
#        rep = ""
#        for row in range(self._dim):
#            for col in range(self._dim):
#                rep += STRMAP[self._board[row][col]]
#                if col == self._dim - 1:
#                    rep += "\n"
#                else:
#                    rep += " | "
#            if row != self._dim - 1:
#                rep += "-" * (4 * self._dim - 3)
#                rep += "\n"
#        return rep
#
#    def get_dim(self):
#        """
#        Return the dimension of the board.
#        """
#        return self._dim
#    
#    def square(self, row, col):
#        """
#        Return the status (EMPTY, PLAYERX, PLAYERO) of the square at
#        position (row, col).
#        """
#        return self._board[row][col]
#
#    def get_empty_squares(self):
#        """
#        Return a list of (row, col) tuples for all empty squares
#        """
#        empty = []
#        for row in range(self._dim):
#            for col in range(self._dim):
#                if self._board[row][col] == EMPTY:
#                    empty.append((row, col))
#        return empty
#
#    def move(self, row, col, player):
#        """
#        Place player on the board at position (row, col).
#        Does nothing if board square is not empty.
#        """
#        if self._board[row][col] == EMPTY:
#            self._board[row][col] = player
#
#    def check_win(self):
#        """
#        If someone has won, return player.
#        If game is a draw, return DRAW.
#        If game is in progress, return None.
#        """
#        lines = []
#
#        # rows
#        lines.extend(self._board)
#
#        # cols
#        cols = [[self._board[rowidx][colidx] for rowidx in range(self._dim)]
#                for colidx in range(self._dim)]
#        lines.extend(cols)
#
#        # diags
#        diag1 = [self._board[idx][idx] for idx in range(self._dim)]
#        diag2 = [self._board[idx][self._dim - idx -1] 
#                 for idx in range(self._dim)]
#        lines.append(diag1)
#        lines.append(diag2)
#
#        # check all lines
#        for line in lines:
#            if len(set(line)) == 1 and line[0] != EMPTY:
#                if self._reverse:
#                    return switch_player(line[0])
#                else:
#                    return line[0]
#
#        # no winner, check for draw
#        if len(self.get_empty_squares()) == 0:
#            return DRAW
#
#        # game is still in progress
#        return None
#            
#    def clone(self):
#        """
#        Return a copy of the board.
#        """
#        return TTTBoard(self._dim, self._reverse, self._board)
#
#
#def switch_player(player):
#    """
#    Convenience function to switch players.
#    
#    Returns other player.
#    """
#    if player == PLAYERX:
#        return PLAYERO
#    else:
#        return PLAYERX
#
#def play_game(mc_move_function, ntrials, reverse = False):
#    """
#    Function to play a game with two MC players.
#    """
#    # Setup game
#    board = TTTBoard(3, reverse)
#    curplayer = PLAYERX
#    winner = None
#    
#    # Run game
#    while winner == None:
#        # Move
#        row, col = mc_move_function(board, curplayer, ntrials)
#        board.move(row, col, curplayer)
#
#        # Update state
#        winner = board.check_win()
#        curplayer = switch_player(curplayer)
#
#        # Display board
#        print board
#        print
#        
#    # Print winner
#    if winner == PLAYERX:
#        print "X wins!"
#    elif winner == PLAYERO:
#        print "O wins!"
#    elif winner == DRAW:
#        print "Tie!"
#    else:
#        print "Error: unknown winner"
