# Player module for COMP30024: Artificial Intelligence, 2018
# Authors: Ckyever Gaviola, Samuel Fatone

from watchyourback import Board, Piece
import random

DEFAULT_BOARD_SIZE = 8
MOVING_PHASE = 24
SHRINK = [128, 129, 192, 193]
WHITE, BLACK = ['O', '@']
PLACING, MOVING = ['placing', 'moving']

class Player:
    def __init__(self, colour):
        if colour == 'white':
            self.colour = WHITE
            self.enemy = BLACK
        if colour == 'black':
            self.colour = BLACK
            self.enemy = WHITE
        self.board = Board(DEFAULT_BOARD_SIZE)
        self.phase = PLACING
        
    # Returns next move
    def action(self, turns):
        print("My board")
        self.board.print_grid()
        print("====================")
        
        next_action = None  # default value if no moves available
        
        # Check if board has shrunk
        if turns in SHRINK:
            self.board.shrink()
            
        # Placing phase
        if self.phase == PLACING:
            start_zone = self.board.starting_zone(self.colour)
            
            # Keep trying to place a piece randomly until successful
            # Will always be a valid action during placing phase
            while True:
                next_action = random.choice(start_zone)
                if (self.board.place_piece(self.colour, next_action) != None):
                    break
        
        # Moving phase
        elif self.phase == MOVING: 
            # Keep randomly choosing a piece until one has available moves
            # then randomly select one of those moves
            while True:
                team = list(self.board.get_alive(self.colour).values())
                piece = random.choice(team)
                # All moves listed are valid
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
        
        return next_action
    
    # Update game board with opponents move
    def update(self, action):
        
        # First element of action has length 1, indicating it is a placing move
        if isinstance(action[0], int):
            self.board.place_piece(self.enemy, action)
        
        # Otherwise must be a nested tuples indicating a move    
        else:
            oldpos, newpos = action
            piece = self.board.get_piece(oldpos)
            piece.make_move(newpos)
            