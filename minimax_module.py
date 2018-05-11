  
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
PLACE_DEPTH = 1
MOVE_DEPTH = 0

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
        
        # Time to shrink the board
        if turns in SHRINK:
            self.board.shrink()
            
        # Placing phase
        if self.phase == PLACING:
            
            # Choose square to place next piece on
            next_action = self.alpha_beta_place()
            
            # Place piece on our representation of the game board
            self.board.place_piece(self.colour, next_action)
        
        # Moving phase
        elif self.phase == MOVING: 
            
            # Choose piece (oldpos) and square to move it to (newpos)
            next_action = self.alpha_beta_move()
            oldpos, newpos = next_action
            
            # Move piece on our representation of the game board
            self.board.get_piece(oldpos).make_move(newpos)
            
        # Check if this was our last turn in placing phase
        if (turns == MOVING_PHASE-2 or turns == MOVING_PHASE-1) and \
        self.phase == PLACING:
            self.phase = MOVING
        
        # Increment our turn count for update function
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
        
        # First check for end game conditions
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
        value += len(board.get_alive(self.enemy)) * -15.0
        
        # How good is our positioning (closer to middle 4 squares is favoured)
        for piece in board.get_alive(self.colour).values():
            # Return distance of middle square it is closest to
            dfm = distance_from_middle = []
            for square in MIDDLE_SQUARES:
                dfm.append(manhattan_distance(piece.pos, square))
            distance = min(dfm)
            
            # Lower the value the more further our pieces are from the centre
            value += distance * -1.0
            
        return value
            
    # Minimax with alpha-beta pruning (for placing phase)
    def alpha_beta_place(self):
        values = {} # dictionary of placing moves and their minimax value
        
        # Iterate through all possible placing moves for current board state
        for pos in self.board.starting_zone(self.colour):
            # Check square isn't already taken
            if self.board.get_piece(pos) == None:
                # Find minimax value
                eliminated = self.board.place_piece(self.colour, pos)
                values[pos] = self.max_place(PLACE_DEPTH, -math.inf, math.inf)
                self.board.undo_place(self.colour, pos, eliminated)
        
        # Return placing move with highest minimax value
        return max(values, key=values.get)
    
    # Returns highest minimax value for our player's turn (MAX)
    def max_place(self, depth, a, b):
        values = []
        
        # Cutoff test: either we've reached end of placing phase or depth limit
        if (self.turns + (PLACE_DEPTH-depth)) >= MOVING_PHASE or depth == 0:
            return self.evaluate_board(self.board)
        
        # Find minimax value of each possible placing move
        for pos in self.board.starting_zone(self.colour):
            if self.board.get_piece(pos) == None:
                eliminated = self.board.place_piece(self.colour, pos)
                a = max(a, self.min_place(depth-1, a, b))
                self.board.undo_place(self.colour, pos, eliminated)
                
                # Alpha-beta pruning
                if a >= b:
                    return b
                
        return a
    
    # Returns lowest minimax value for opponents turn (MIN)
    def min_place(self, depth, a, b):
        values = []
        
        # Cutoff test (same as above)
        if (self.turns + (PLACE_DEPTH-depth)) >= MOVING_PHASE or depth == 0:
            return self.evaluate_board(self.board)
    
        # Find minimax value of each possible placing move
        for pos in self.board.starting_zone(self.enemy):
            if self.board.get_piece(pos) == None:
                eliminated = self.board.place_piece(self.enemy, pos)
                b = min(b, self.max_place(depth-1, a, b))
                self.board.undo_place(self.enemy, pos, eliminated)
                
                # Alpha-beta pruning
                if b <= a:
                    return a
                
        return b

    # Minimax with alpha-beta pruning (for moving phase)
    def alpha_beta_move(self):
        values = {} # dictionary of moves and corresponding minimax values
        
        # Iterate through possible moves for each of our pieces
        for piece in self.board.get_alive(self.colour).values():
            for move in piece.listmoves():
                oldpos = piece.pos
                eliminated = piece.make_move(move)
                values[oldpos, move] = self.max_move(MOVE_DEPTH, -math.inf, math.inf)
                piece.undo_move(oldpos, eliminated) 
        
        return max(values, key=values.get)
    
    # Returns highest minimax value for our player's turn (MAX)
    def max_move(self, depth, a, b):
        values = []
        
        # Cutoff test: reached end game condition or depth limit
        if self.board.check_win(self.colour) != CONTINUE or depth == 0:
            return self.evaluate_board(self.board)
        
        # Iterate through each move for each of MAX's pieces
        for piece in self.board.get_alive(self.colour).values():
            for move in piece.listmoves():
                oldpos = piece.pos
                eliminated = piece.make_move(move)
                a = max(a, self.min_move(depth-1, a, b))
                piece.undo_move(oldpos, eliminated)
                
                # Alpha-beta pruning
                if a >= b:
                    return b
                
        return a
    
    # Returns lowest minimax value for opponents turn (MIN)
    def min_move(self, depth, a, b):
        values = []
        
        # Cutoff test (same as above)
        if self.board.check_win(self.colour) != CONTINUE or depth == 0:
            return self.evaluate_board(self.board)
        
        # Iterate through each move for each of MIN's pieces
        for piece in self.board.get_alive(self.enemy).values():
            for move in piece.listmoves():
                oldpos = piece.pos
                eliminated = piece.make_move(move)
                b = min(b, self.max_move(depth-1, a, b))
                piece.undo_move(oldpos, eliminated)
                
                # Alpha-beta pruning
                if b <= a:
                    return a
                
        return b