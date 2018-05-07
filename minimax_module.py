# Player module for COMP30024: Artificial Intelligence, 2018
# Authors: Ckyever Gaviola, Samuel Fatone
# Strategy: Use evaluation function with minimax and alpha-beta pruning

from watchyourback import Board, Piece
import random

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

class Player:
    def __init__(self, colour):
        if colour == 'white':
            self.colour = WHITE
            self.enemy = BLACK
            self.team = self.board.white_pieces
        if colour == 'black':
            self.colour = BLACK
            self.enemy = WHITE
            self.team = self.board.black_pieces
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
            
    # Evaluation function that returns the utility value for the current 
    # board state
    
    def evaluate_board(self):
        value = 0.0
        
        # First check win conditions
        result = self.board.check_win(self.colour)
        if result == WIN:
            return 1000
        elif result == LOSS:
            return -1000
        # Should only take a draw if other moves lead to a very low value
        elif result == TIE:
            return -100 
        
        # Compare number of our pieces to number of enemy pieces
        # Give more value to our pieces (defensive strategy)
        value += self.board.get_alive(self.colour) * 20.0
        value += self.board.get_alive(self.enemy) * -20.0
        
        # How good is our positioning (closer to middle 4 squares is favoured)
        for piece in self.team:
            # Return distance of middle square it is closest to
            dfm = distance_from_middle = []
            for square in MIDDLE_SQUARES:
                dfm.append(manhattan_distance(piece.pos, sqaure))
            distance = min(dfm)
            # Penalise board state the further a piece is from middle 4
            value += distance * -1.0
            
        return value