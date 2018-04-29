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
    # Class representing board as a dictionary ('grid' = {(x,y): '-', ...}) &
    # keeping track of pieces (instance of Piece) with a similar dictionary
    # ('white_pieces' = {(x,y): piece, ...})
    def __init__(self):
        # Initialise default size board (8x8) with empty squares, then insert 
        # corners after
        self.grid = {}
        for y, row in enumerate(range(8)):
            for x, char in enumerate(range(8)):
                self.grid[x, y] = EMPTY
        for corner in [(0,0), (0,7), (7,0), (7,7)]:
            self.grid[corner] = CORNER
            
        # Initialise dictionary holding each players pieces
        self.white_pieces = {}
        self.black_pieces = {}
        
    def place_piece(self, colour, pos):
        # Returns true if piece placed successfully
        # colour (BLACK/WHITE), pos (x,y)
        
        if pos in self.grid:
            if self.grid[pos] == EMPTY:
                if colour == WHITE:
                    self.white_pieces[pos] = (Piece(WHITE, pos, self))
                    self.grid[pos] = WHITE
                if colour == BLACK:
                    self.black_pieces[pos] = (Piece(BLACK, pos, self))
                    self.grid[pos] = BLACK
                return True
            
        return False
    
    def remove_piece(self, pos):
        # Remove piece from grid
        if pos in self.grid:
            self.grid[pos] = EMPTY
        
    def print_board(self):
        # Testing purposes only. 
        # Prints out physical representation of game board 
        size = range(8)
        print('\n'.join(' '.join(self.grid[x,y] for x in size) for y in size))
            
class Piece:
    # Class representing each piece in terms of player (WHITE/BLACK), 
    # pos (x,y), board (instance of Board it belongs to), alive (whether
    # or not it is on the board) and its enemies (WHITE/BLACK)
    def __init__(self, player, pos, board):
        self.player = player
        self.pos = pos
        self.board = board
        self.alive = True
        if player == WHITE:
            self.enemy = [BLACK, CORNER]
        else:
            self.enemy = [WHITE, CORNER]
        
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
    
    def check_eliminated(self):
        # Returns true if eliminated and removes piece from 'grid' 
        # and sets alive = False
        for forward, backward in [(UP, DOWN), (LEFT, RIGHT)]:
            front_square = step(self.pos, forward)
            back_square = step(self.pos, backward)
            if front_square in self.board.grid \
            and back_square in self.board.grid:
                if self.board.grid[front_square] in self.enemy \
                and self.board.grid[back_square] in self.enemy:
                    self.board.remove_piece(self.pos)
                    self.alive = False
                    return True
                    
    def resurrect(self):
        # Places piece back on board and sets alive = True
        self.board.grid[self.pos] = self.player
        self.alive = True
                    
    def make_move(self, newpos):
        # Attempts to move piece to new position and check for eliminations.
        # Returns eliminated pieces as a list to enable undomove()
        oldpos = self.pos
        self.pos = newpos   
        self.board.grid[oldpos] = EMPTY
        self.board.grid[newpos] = self.player
        
        eliminated_pieces = []
        if self.player == WHITE:
            enemy_pieces = self.board.black_pieces
        else:
            enemy_pieces = self.board.white_pieces
            
        # Eliminate any surrounding pieces if it is the case
        for direction in DIRECTIONS:
            adjacent_square = step(self.pos, direction)
            if adjacent_square in self.board.grid:
                if self.board.grid[adjacent_square] == self.enemy[0]:
                    if enemy_pieces[adjacent_square].check_eliminated():
                        eliminated_pieces.append(enemy_pieces[adjacent_square])
                
        # Now check if piece has itself been eliminated
        self.check_eliminated()
                 