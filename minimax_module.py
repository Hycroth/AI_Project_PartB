# Player module for COMP30024: Artificial Intelligence, 2018
# Authors: Ckyever Gaviola, Samuel Fatone
# Strategy: Use evaluation function with minimax and alpha-beta pruning

from watchyourback import Board, Piece
import random, math, copy

DEFAULT_BOARD_SIZE = 8
MOVING_PHASE = 24
SHRINK = [128, 192]
WHITE, BLACK = ['O', '@']
PLACING, MOVING = ['placing', 'moving']
WIN, TIE, LOSS, CONTINUE = [3,2,1,0]
MIDDLE_SQUARES = [(3,3), (4,3), (3,4), (4,4)]

# HELPER FUNCTION
def manhattan_distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(ay - by) + abs(ax - bx)

# CLASSES

# Class representing our Watch Your Back AI
class Player:
    def __init__(self, colour):
        self.board = Board(DEFAULT_BOARD_SIZE)
        self.phase = PLACING
        self.turns = 0
        
        if colour == 'white':
            self.colour = WHITE
            self.enemy = BLACK
        if colour == 'black':
            self.colour = BLACK
            self.enemy = WHITE
        
    # Returns next move
    def action(self, turns):
        next_action = None  # default value if no moves available
        self.turns = turns # allow us to know when to shrink in update function
        
        # Check if board has shrunk
        if turns in SHRINK:
            self.board.shrink()
            
        # Placing phase
        if self.phase == PLACING:
            
            # Using minimax
            #next_action = self.minimax_decision()
            #self.board.place_piece(self.colour, next_action)
            
            # Using minimax with alpha-beta pruning
            next_action = self.alpha_beta_search()
            self.board.place_piece(self.colour, next_action)
        
        # Moving phase
        elif self.phase == MOVING: 
            # Keep randomly choosing a piece until one has available moves
            # then randomly select one of those moves
            while True:
                team = list(self.board.get_alive(self.colour).values())
                
                # In the case board shrink eliminates all of our team
                if not team:
                    break
                
                # Choose random piece and a random move
                piece = random.choice(team)
                moves = piece.listmoves()
                
                # Check piece has moves available, then make move
                if moves:
                    newpos = random.choice(moves)
                    next_action = (piece.pos, newpos)
                    piece.make_move(newpos)
                    break
        
        # Check if this was our last turn in placing phase
        if (turns == MOVING_PHASE-2 or turns == MOVING_PHASE-1) and \
        self.phase == PLACING:
            self.phase = MOVING
        
        # Output testing
        #print("====================\n" + self.colour + "'s board")
        #self.board.print_grid()
        #print("White:" + str(self.board.get_alive('O').keys()))
        #print("Black:" + str(self.board.get_alive('@').keys()))
        print("Value of board for white = " + str(self.evaluate_board(self.board)))
        #print("====================\nReferee's board")
        
        self.turns += 1
        return next_action
    
    # Update game board with opponents move
    def update(self, action):
        # Check if board has shrunk
        if self.turns in SHRINK:
            self.board.shrink()
        
        # First element of action has length 1, indicating it is a placing move
        if isinstance(action[0], int):
            self.board.place_piece(self.enemy, action)
        
        # Otherwise must be a nested tuples indicating a move    
        else:
            oldpos, newpos = action
            piece = self.board.get_piece(oldpos)
            piece.make_move(newpos)
                    
    # Evaluation function that returns the utility value for a given 
    # board state for this player
    def evaluate_board(self, board):
        value = 0.0
        
        # First check win conditions if we are in moving phase
        if self.phase == MOVING:
            result = board.check_win(self.colour)
            if result == WIN:
                return math.inf
            elif result == LOSS:
                return -math.inf
            # Should only take a draw if other moves lead to a very low value
            elif result == TIE:
                return -100 
        
        # Compare number of our pieces to number of enemy pieces
        # Give more value to our pieces (defensive strategy)
        value += len(board.get_alive(self.colour)) * 20.0
        value += len(board.get_alive(self.enemy)) * -10.0
        
        # How good is our positioning (closer to middle 4 squares is favoured)
        for piece in board.get_alive(self.colour).values():
            # Return distance of middle square it is closest to
            dfm = distance_from_middle = []
            for square in MIDDLE_SQUARES:
                dfm.append(manhattan_distance(piece.pos, square))
            distance = min(dfm)
            # Penalise board state more the further our pieces are from 
            # middle 4 squares
            value += distance * -1.0
            
        return value
    
    # Only for placing phase for now, gets the move with highest minimax value
    def minimax_decision(self):
        values = {} # Key - move, Value - Minimax value
        
        # Iterate through all possible placing moves for current board state
        for pos in self.board.starting_zone(self.colour):
            # Check square isn't already taken
            if self.board.get_piece(pos) == None:
                # Find minimax value of move up to 2 ply
                eliminated = self.board.place_piece(self.colour, pos)
                values[pos] = self.minimax_value(self.board, self.colour, 2)
                self.board.undo_place(self.colour, pos, eliminated)
        
        return max(values, key=values.get)
    
    # Returns minimax value given that it is 'player's turn
    def minimax_value(self, board, player, depth):
        # Terminal test or we've hit search depth
        if self.board.check_win(self.colour) != CONTINUE or depth == 0:
            return self.evaluate_board(board)
        
        # Lists our successor board states depending on whose turn it is
        values = []
        for pos in self.board.starting_zone(player):
            if self.board.get_piece(pos) == None:
                eliminated = self.board.place_piece(player, pos)
                values.append(self.minimax_value(board, player, depth-1))
                self.board.undo_place(player, pos, eliminated)
                
        # MAX's (our AI) turn
        if player == self.colour:
            return max(values)
        
        # MIN's (opponent) turn
        elif player == self.enemy:
            return min(values)
            
    # Minimax but with alpha-beta pruning
    def alpha_beta_search(self):
        values = {} # Key - move, Value - Minimax value
        
        # Iterate through all possible placing moves for current board state
        for pos in self.board.starting_zone(self.colour):
            # Check square isn't already taken
            if self.board.get_piece(pos) == None:
                # Find minimax value
                eliminated = self.board.place_piece(self.colour, pos)
                values[pos] = self.max_value(self.board, self.colour, 2,
                                              -math.inf, math.inf)
                self.board.undo_place(self.colour, pos, eliminated)
        
        return max(values, key=values.get)
        
    
    # The following two functions are for Alpha-beta pruning
    def max_value(self, board, player, depth, a, b):
        # Cutoff test
        if self.board.check_win(self.colour) != CONTINUE or depth == 0:
            return self.evaluate_board(board)
        
        values = []
        for pos in self.board.starting_zone(player):
            if self.board.get_piece(pos) == None:
                eliminated = self.board.place_piece(player, pos)
                a = max(a, self.min_value(board, player, depth-1, a, b))
                self.board.undo_place(player, pos, eliminated)
                if a >= b:
                    return b
                
        return a
    
    # The following two functions are for Alpha-beta pruning
    def min_value(self, board, player, depth, a, b):
        # Cutoff test
        if self.board.check_win(self.colour) != CONTINUE or depth == 0:
            return self.evaluate_board(board)
        
        values = []
        for pos in self.board.starting_zone(player):
            if self.board.get_piece(pos) == None:
                eliminated = self.board.place_piece(player, pos)
                b = min(b, self.max_value(board, player, depth-1, a, b))
                self.board.undo_place(player, pos, eliminated)
                if b <= a:
                    return a
                
        return b