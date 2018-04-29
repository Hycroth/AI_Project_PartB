# Piece module for COMP30024: Artificial Intelligence, 2018
# Authors: Ckyever Gaviola, Samuel Fatone
# Note: Some ideas have been borrowed from the sample-solution

# CONSTANTS
WHITE, BLACK, CORNER, EMPTY = ['O','@','X','-']
DIRECTIONS = UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

# HELPER FUNCTIONS

# Takes position (x,y) and applies direction (from DIRECTIONS) and returns
# the resulting tuple
def step(position, direction):
    px, py = position
    dx, dy = direction
    return (px+dx, py+dy)

# CLASSES

class Board:
    # Class representing game board as a dictionary ('grid' = {(x,y): '-', ...}) &
    # keeping track of each players pieces in lists ('white_pieces','black_pieces')
    def __init__(self):
        # Initialise default size board (8x8) with empty squares, then insert 
        # corners after
        self.grid = {}
        for y, row in enumerate(range(8)):
            for x, char in enumerate(range(8)):
                self.grid[x, y] = EMPTY
        for corner in [(0,0), (0,7), (7,0), (7,7)]:
            self.grid[corner] = CORNER
            
        # Initialise lists holding each players pieces
        self.white_pieces = []
        self.black_pieces = []
        
    def place_piece(self, colour, pos):
        # Returns true if piece placed successfully
        # colour (BLACK/WHITE), pos (x,y)
        
        if pos in self.grid:
            if self.grid[pos] == EMPTY:
                if colour == WHITE:
                    self.white_pieces.append(Piece(WHITE, pos, self))
                    self.grid[pos] = WHITE
                if colour == BLACK:
                    self.black_pieces.append(Piece(BLACK, pos, self))
                    self.grid[pos] = BLACK
                return True
            
        return False
        
    def print_board(self):
        # Testing purposes only. 
        # Prints out physical representation of game board 
        size = range(8)
        print('\n'.join(' '.join(self.grid[x,y] for x in size) for y in size))
            
class Piece:
    # Class representing each piece in terms of player (WHITE/BLACK), 
    # pos (x,y), board (instance of Board it belongs to) and alive (whether
    # or not it is on the board)
    def __init__(self, player, pos, board):
        self.player = player
        self.pos = pos
        self.board = board
        self.alive = True
        
    def listmoves(self):
        # Return all available moves as a list
        moves = []
        for dir in DIRECTIONS:
            # Try make a normal move
            adjacent_square = step(self.pos, dir)
            if adjacent_square in self.board.grid:
                if self.board.grid[adjacent_square] == EMPTY:
                    moves.append(adjacent_square)
                    continue # Since jump is not possible
                
            # If not try jump to square next to adjacent square
            jump_square = step(adjacent_square, dir)
            if jump_square in self.board.grid:
                if self.board.grid[jump_square] == EMPTY:
                    moves.append(jump_square)
                    
        return moves