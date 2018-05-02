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
    def __init__(self, size):
        # Initialise blank board with dimensions size x size then insert 
        # corners after. Also initialise list 'playingarea' holding all tuples
        # included in the active zone (allows us to shrink board easier)
        self.grid = {}
        self.playingarea = []
        self.playingsize = size
        for y, row in enumerate(range(size)):
            for x, char in enumerate(range(size)):
                self.grid[x, y] = EMPTY
                self.playingarea.append((x,y))
        for corner in [(0,0), (0,size-1), (size-1,0), (size-1,size-1)]:
            self.grid[corner] = CORNER
            
        # Initialise dictionary holding each players pieces
        self.white_pieces = {}
        self.black_pieces = {}
        
    def place_piece(self, colour, pos):
        # Returns true if piece placed successfully
        # colour (BLACK/WHITE), pos (x,y)
        
        if pos in self.playingarea:
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
        
    def update_team(self, colour, newpos, oldpos):
        # Updates the key value of a piece in its respective dictionary
        if colour == WHITE:
            dictionary = self.white_pieces
        else:
            dictionary = self.black_pieces
            
        dictionary[newpos] = dictionary[oldpos]
        del dictionary[oldpos]
    """   
    def shrink(self):
        # Shrink the play area and make any required eliminations
        top, _ = self.playingarea[0]  # Top left corner ('X')
        bottom = self.playingsize - 1
        
        # Iterate through outside border
        for square in range(top, playingsize):
            for border in [top, bottom]:
                # Top then bottom row (since borders overlap
                # check square has not been removed already)
                if (border, square) in self.playingarea:
                    self.playingarea.remove((border,square))
                    for pieces in [self.white_pieces, self.black_pieces]:
                        if (border, square) in pieces:
                            pieces[(border, square)].check_elim 
                # Left then right column
                if (square, border) in self.playingarea:
                    self.playingarea.remove((square,border))
        
        # Replace existing corners with '-'
        for corner in [(top, top), (bottom, top), (top, bottom), (bottom, bottom)]:
            self.grid[corner] = EMPTY
            
        # Add new corners
        top += 1
        bottom -= 1
        for corner in [(top, top), (bottom, top), (top, bottom), (bottom, bottom)]:
            self.grid[corner] = CORNER
            
        # Check if any pieces eliminated by new corners (top left moving 
        # counterclockwise)
        
        # Change size of playable area    
        self.playingsize -= 2    
    """       
    def print_grid(self):
        # Testing purposes only. 
        # Prints out physical representation of game board 
        size = range(self.playingsize)
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
            if adjacent_square in self.board.playingarea:
                if self.board.grid[adjacent_square] == EMPTY:
                    moves.append(adjacent_square)
                    continue # Since jump is not possible
                
            # If not try jump to square next to adjacent square
            jump_square = step(adjacent_square, dir)
            if jump_square in self.board.playingarea:
                if self.board.grid[jump_square] == EMPTY:
                    moves.append(jump_square)
                    
        return moves
    
    def check_eliminated(self):
        # Returns true if eliminated and removes piece from 'grid' 
        # and sets alive = False
        for forward, backward in [(UP, DOWN), (LEFT, RIGHT)]:
            front_square = step(self.pos, forward)
            back_square = step(self.pos, backward)
            if front_square in self.board.playingarea \
            and back_square in self.board.playingarea:
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
        # Moves piece to new position and check for eliminations.
        # Returns eliminated pieces as a list to enable undomove()
        oldpos = self.pos
        self.pos = newpos   
        self.board.grid[oldpos] = EMPTY
        self.board.grid[newpos] = self.player
        self.board.update_team(self.player, newpos, oldpos)
        
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
        if self.check_eliminated():
            eliminated_pieces.append(self)
            
        return eliminated_pieces
        
    def undo_move(self, oldpos, eliminated):
        # Move piece back to 'oldpos' and resurrect 'eliminated' pieces
        for piece in eliminated:
            piece.resurrect()
            
        newpos = self.pos
        self.pos = oldpos
        self.board.grid[newpos] = EMPTY
        self.board.grid[oldpos] = self.player
                 