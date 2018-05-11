"""
Class representing a player for a game of Watch Your Back! using referee.py

As per the project spec it can return the next action, either a single tuple 
(placing piece) or 2 tested tuples (moving piece), and receive an opponents
action.

This class also contains algorithms and evaluations functions which implement
the search strategies to be used when deciding the next action. The logic
for these functions have been based on code shown in the lecture slides (AIMA)
and the textbook "Artificial Intelligence: A Modern Approach"

Authors: Ckyever Gaviola, Samuel Fatone
May 2018
"""
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
    """
    Takes two tuples (ax,ay) and (bx,by) and returns the Manhattan distance
    between the two
    """
    ax, ay = a
    bx, by = b
    return abs(ay - by) + abs(ax - bx)

# CLASSES
class Player:
    """
    A class which represents our AI player which makes moves based on its
    own internal representation of the game board and also updates it with
    opponent's moves
    """
    def __init__(self, colour):
        """
        Creates a new board and sets the phase and turns to indicate the
        beginning of a game. It also identifies what colour/symbol it is
        playing and the colour/symbol of its opponent
        """
        self.board = Board(DEFAULT_BOARD_SIZE)
        self.phase = PLACING
        self.turns = 0
        
        if colour == 'white':
            self.colour = WHITE
            self.enemy = BLACK
        if colour == 'black':
            self.colour = BLACK
            self.enemy = WHITE
        
    def action(self, turns):
        """
        Given the number of turns into the current phase of the game, returns
        its next action (either placing a piece (x,y) or moving one 
        ((a,b),(c,d)) ) and updates the internal game board. Also shrinks the
        board when it has reached that point in the game
        """
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
            # Variable which will determine whether moves to a border piece will be allowed 
            exclude_borders = 0
            
            while True:
                # If the number of turns for the colour is less than or equal to the number of pieces on the border,
                # will move them first
                if self.board.count_outside(self.colour) >= (SHRINK[0] - self.turns)/2 and self.turns < SHRINK[0]:
                    team = list(self.board.get_border_pieces(self.colour).values())
                    exclude_borders = 1
                elif self.board.count_outside(self.colour) >= (SHRINK[1] - self.turns)/2 and self.turns < SHRINK[1]:
                    team = list(self.board.get_border_pieces(self.colour).values())
                    exclude_borders = 1
                    
                # If not use default move strategy
                else:
                    # Choose piece (oldpos) and square to move it to (newpos)
                    next_action = self.alpha_beta_move()
                    oldpos, newpos = next_action
            
                    # Move piece on our representation of the game board
                    self.board.get_piece(oldpos).make_move(newpos)
                    break
                
                # In the case board shrink eliminates all of our team
                if not team:
                    break
                
                # Choose random piece and a random move
                while True:
                    piece = random.choice(team)
                    moves = piece.listmoves(exclude_borders)
                    if len(moves) > 0:
                        break
                
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
        
        # Increment our turn count to ensure update shrinks at the right time
        self.turns += 1
        
        return next_action

    def update(self, action):
        """
        Updates the internal game board with opponents "action" and shrinks the
        board if it has reached that point in the game
        """
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
        """
        Given an instance of Board returns a utility value based on the
        number of pieces alive on each team and positioning of our pieces
        relative to the middle of the board
        """
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
            
    def alpha_beta_place(self):
        """
        Wrapper function for minimax with alpha-beta pruning which returns the
        placing move with the highest minimax value by recursion
        """
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
    
    def max_place(self, depth, a, b):
        """
        Finds highest minimax value for each possible action during our 
        player's (MAX) turn
        """
        # Cutoff test: either we've reached end of placing phase or depth limit
        if (self.turns + (PLACE_DEPTH-depth)) >= MOVING_PHASE or depth == 0:
            return self.evaluate_board(self.board)
        
        # Iterate through each placing move
        for pos in self.board.starting_zone(self.colour):
            if self.board.get_piece(pos) == None:
                eliminated = self.board.place_piece(self.colour, pos)
                a = max(a, self.min_place(depth-1, a, b))
                self.board.undo_place(self.colour, pos, eliminated)
                
                # Alpha-beta pruning
                if a >= b:
                    return b
                
        return a
    
    def min_place(self, depth, a, b):
        """
        Returns the lowest minimax value for each possible action during
        opponent's (MIN) turn
        """
        # Cutoff test (same as max_place)
        if (self.turns + (PLACE_DEPTH-depth)) >= MOVING_PHASE or depth == 0:
            return self.evaluate_board(self.board)
    
        # Iterate through each placing move
        for pos in self.board.starting_zone(self.enemy):
            if self.board.get_piece(pos) == None:
                eliminated = self.board.place_piece(self.enemy, pos)
                b = min(b, self.max_place(depth-1, a, b))
                self.board.undo_place(self.enemy, pos, eliminated)
                
                # Alpha-beta pruning
                if b <= a:
                    return a
                
        return b

    def alpha_beta_move(self):
        """
        Wrapper function for minimax with alpha-beta pruning for moving phase.
        Only slightly different to placing algorithm would be better to merge
        these two functions somehow.
        """
        values = {} # dictionary of moves and corresponding minimax values
        
        # Iterate through possible moves for each of our pieces
        for piece in self.board.get_alive(self.colour).values():
            for move in piece.listmoves(0):
                oldpos = piece.pos
                eliminated = piece.make_move(move)
                values[oldpos, move] = self.max_move(MOVE_DEPTH, -math.inf, math.inf)
                piece.undo_move(oldpos, eliminated) 
        
        return max(values, key=values.get)
    
    def max_move(self, depth, a, b):
        """
        Finds highest minimax value for each possible action during our 
        player's (MAX) turn
        """
        # Cutoff test: reached end game condition or depth limit
        if self.board.check_win(self.colour) != CONTINUE or depth == 0:
            return self.evaluate_board(self.board)
        
        # Iterate through each move for each of MAX's pieces
        for piece in self.board.get_alive(self.colour).values():
            for move in piece.listmoves(0):
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
        """
        Returns the lowest minimax value for each possible action during
        opponent's (MIN) turn
        """
        # Cutoff test (same as above)
        if self.board.check_win(self.colour) != CONTINUE or depth == 0:
            return self.evaluate_board(self.board)
        
        # Iterate through each move for each of MIN's pieces
        for piece in self.board.get_alive(self.enemy).values():
            for move in piece.listmoves(0):
                oldpos = piece.pos
                eliminated = piece.make_move(move)
                b = min(b, self.max_move(depth-1, a, b))
                piece.undo_move(oldpos, eliminated)
                
                # Alpha-beta pruning
                if b <= a:
                    return a
                
        return b