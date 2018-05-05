# Player module for COMP30024: Artificial Intelligence, 2018
# Authors: Ckyever Gaviola, Samuel Fatone

from watchyourback import Board, Piece
import random

DEFAULT_BOARD_SIZE = 8
MOVING_PHASE = 24
SHRINK = [152, 216]
WHITE, BLACK = ['O', '@']

class Player:
    def __init__(self, colour):
        if colour == 'white':
            self.colour = WHITE
            self.enemy = BLACK
        if colour == 'black':
            self.colour = BLACK
            self.enemy = WHITE
        self.board = Board(DEFAULT_BOARD_SIZE)
        
    # Returns next move
    def action(self, turns):
        next_action = None  # default value if no moves available
        
        # Check if board shrinks
        if turns in SHRINK:
            self.board.shrink()
            
        # Placing phase
        if turns <= MOVING_PHASE:
            start_zone = self.board.starting_zone(self.colour)
            
            # Keep trying to place a piece randomly until successful
            # Will always be a valid action during placing phase
            while True:
                next_action = random.choice(start_zone)
                if (self.board.place_piece(self.colour, next_action) != None):
                    break
        
        # Moving phase
        else: 
            # Keep randomly choosing a piece until one has available moves
            # then randomly select one of those moves
            while True:
                piece = random.choice(self.board.get_alive(self.colour))
                # All moves listed are valid
                moves = piece.listmoves()
                
                # Check piece has moves available, then make move
                if moves:
                    newpos = random.choice(moves)
                    piece.make_move(newpos)
                    next_action = (piece.pos, newpos)
                    break
        
        return next_action
    
    # Update game board with opponents move
    def update(self, action):
        
        # Action specifies a placing move
        if len(action) == 1:
            self.board.place_piece(self.enemy, action)
        
        # Action has nested tuples indicating a move    
        else:
            oldpos, newpos = action
            piece = self.board.get_piece(oldpos)
            piece.make_move(newpos)
            