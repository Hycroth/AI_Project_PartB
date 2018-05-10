# Player module for COMP30024: Artificial Intelligence, 2018
# Authors: Ckyever Gaviola, Samuel Fatone

from watchyourback import Board, Piece
import random

DEFAULT_BOARD_SIZE = 8
MOVING_PHASE = 24
SHRINK = [128, 192]
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
        self.turns = 0
        
    # Returns next move
    def action(self, turns):
        next_action = None  # default value if no moves available
        self.turns = turns # allow us to know when to shrink in update function
        
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
            
            exclude_borders = 0
            
            while True:
                if self.board.count_outside(self.colour) >= (SHRINK[0] - self.turns)/2 and self.turns < SHRINK[0]:
                    team = list(self.board.get_border_pieces(self.colour).values())
                    exclude_borders = 1
                elif self.board.count_outside(self.colour) >= (SHRINK[1] - self.turns)/2 and self.turns < SHRINK[1]:
                    team = list(self.board.get_border_pieces(self.colour).values())
                    exclude_borders = 1
                else:
                    team = list(self.board.get_alive(self.colour).values())
                
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
            
