"""
Classes representing the game board used in Watch Your Back! and the pieces 
moving around it

Created to simulate all valid events that occur during a game of Watch Your 
Back! and also additional informative functions to assist with Player's search 
strategy. It also allows moves to be reversed to aid the Player class.

Authors: Ckyever Gaviola, Samuel Fatone
May 2018
"""
# CONSTANTS
WHITE, BLACK, CORNER, EMPTY = ['O','@','X','-']
DIRECTIONS = UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
WHITE_ZONE, BLACK_ZONE = range(6), range(2, 8)
WIN, TIE, LOSS, CONTINUE = [3,2,1,0]

# HELPER FUNCTIONS
def step(position, direction):
    """
    Takes position (x,y) and applies direction (from DIRECTIONS) and returns
    the resulting tuple
    """
    px, py = position
    dx, dy = direction
    return (px+dx, py+dy)

# CLASSES
class Board:
    """
    A class that represents the game board in Watch Your Back! containing
    functions which give info about certain pieces, shrink the board, and
    place pieces.
    """
    def __init__(self, size):
        """
        Initialise blank board with dimensions size x size then insert 
        corners after. Also initialise list 'playingarea' holding all tuples
        included in the active zone (allows us to shrink board easier) and
        dictionary of each players pieces
        """
        self.grid = {}
        self.size = size
        self.playingarea = []
        self.playingsize = size
        self.numOfShrinks = 0
        for y, row in enumerate(range(size)):
            for x, char in enumerate(range(size)):
                self.grid[x, y] = EMPTY
                self.playingarea.append((x,y))
        for corner in [(0,0), (0,size-1), (size-1,0), (size-1,size-1)]:
            self.grid[corner] = CORNER
            
        # Initialise dictionary holding each players pieces
        self.white_pieces = {}
        self.black_pieces = {}
        
    def starting_zone(self, colour):
        """
        Returns a list which represents all tuples in selected teams zone
        during the placing phase
        """
        zone = []
        
        for x, y in self.playingarea:
            if (x, y) not in [(0,0), (0,7), (7,0), (7,7)]:
                if colour == WHITE:
                    if y in WHITE_ZONE:
                        zone.append((x, y))
                else:
                    if y in BLACK_ZONE:
                        zone.append((x, y))
    
        return zone
    
    def get_piece(self, pos):
        """
        Returns an alive piece at the given position. If no piece, return None
        """
        piece = None
        
        # Is piece white?
        if pos in self.white_pieces and self.white_pieces[pos].alive == True:
            piece = self.white_pieces[pos]
        
        # Is piece black?    
        if pos in self.black_pieces and self.black_pieces[pos].alive == True:
            piece = self.black_pieces[pos]
            
        return piece
    
    def get_alive(self, colour):
        """
        Return dictionary containing pieces that are currently alive
        """
        dictionary = {}
        
        if colour == WHITE:
            for key, piece in self.white_pieces.items():
                if piece.alive == True:
                    dictionary[key] = piece
        else:
            for key, piece in self.black_pieces.items():
                if piece.alive == True:
                    dictionary[key] = piece
                    
        return dictionary
    
    def get_border_pieces(self, colour):
        """
        Gets pieces that are currently on the border if a shrink were to occur
        now
        """
        dictionary = {}
        
        s = self.numOfShrinks
        
        if colour == WHITE:
            for key, piece in self.white_pieces.items():
                if piece.alive == True:
                    if key[0]==s or key[0]==7-s or key[1]==s or key[1]==7-s:
                        dictionary[key] = piece
                    elif (key[0]==s+1 and key[1]==s+1) or \
                    (key[0]==s+1 and key[1]==6-s) or \
                    (key[0]==6-s and key[1]==s+1) or \
                    (key[0]==6-s and key[1]==6-s):
                        dictionary[key] = piece
        else:
            for key, piece in self.black_pieces.items():
                if piece.alive == True:
                    if key[0]==s or key[0]==7-s or key[1]==s or key[1]==7-s:
                        dictionary[key] = piece
                    elif (key[0]==s+1 and key[1]==s+1) or \
                    (key[0]==s+1 and key[1]==6-s) or \
                    (key[0]==6-s and key[1]==s+1) or \
                    (key[0]==6-s and key[1]==6-s):
                        dictionary[key] = piece
                    
        return dictionary
        
    def place_piece(self, colour, pos):
        """
        Returns eliminated pieces (can be empty) if piece placed 
        successfully (to be used for undo_place), else return None
        """
        eliminated_pieces = []
        
        if pos in self.playingarea:
            if self.grid[pos] == EMPTY:
                if colour == WHITE:
                    self.white_pieces[pos] = (Piece(WHITE, pos, self))
                    self.grid[pos] = WHITE
                    eliminated_pieces = \
                    self.white_pieces[pos].eliminate_surrounding()
                elif colour == BLACK:
                    self.black_pieces[pos] = (Piece(BLACK, pos, self))
                    self.grid[pos] = BLACK
                    eliminated_pieces = \
                    self.black_pieces[pos].eliminate_surrounding()    
                return eliminated_pieces
            
        return None
    
    def undo_place(self, colour, pos, eliminated):
        """
        Undo the most recent placing move by specified player
        """
        for piece in eliminated:
            piece.resurrect()
            
        self.remove_piece(pos)    
        if colour == WHITE:
            if pos in self.white_pieces:
                del self.white_pieces[pos]
        else:
            if pos in self.black_pieces:
                del self.black_pieces[pos]
    
    def remove_piece(self, pos):
        """
        Remove pieces character from the grid
        """
        if pos in self.grid:
            self.grid[pos] = EMPTY
        
    def update_team(self, colour, newpos, oldpos):
        """
        Updates the key value of a piece in its respective team dictionary
        """
        if colour == WHITE:
            dictionary = self.white_pieces
        else:
            dictionary = self.black_pieces
            
        dictionary[newpos] = dictionary[oldpos]
        del dictionary[oldpos]
       
    def count_outside(self, colour):
        """
        Counts the number of pieces that would be eliminated if a shrink were
        to occur now
        """
        count = 0
        
        s = self.numOfShrinks
        for i in range(s, 8-s):
            for j in range(s, 8-s):
                if ((i==s or i==7-s or j==s or j==7-s) and \
                    self.grid[i, j] == colour):
                    count += 1
                elif ((i==s+1 and j==s+1) or (i==s+1 and j==6-s) or \
                      (i==6-s and j==s+1) or \
                      (i==6-s and j==6-s)) and self.grid[i, j] == colour:
                    count += 1
        
        return count
    
    def shrink(self):
        """
        Shrink the play area and make any required eliminations.
        Can only be called twice.
        """
        s = self.numOfShrinks
        
        # Iterate through outside borders
        for square in range(s, 8 - s):
            for border in [s, 7 - s]:
                # Top then bottom row
                if (border, square) in self.playingarea:
                    self.playingarea.remove((border,square))
                    for pieces in [self.white_pieces, self.black_pieces]:
                        if (border, square) in pieces:
                            pieces[(border, square)].check_eliminated() 
                # Left then right column
                if (square, border) in self.playingarea:
                    self.playingarea.remove((square,border))
                    for pieces in [self.white_pieces, self.black_pieces]:
                        if (square, border) in pieces:
                            pieces[(square, border)].check_eliminated()
        
        # Replace existing corners with '-'
        for corner in [(s, s), (s, 7-s), (7-s, 7-s), (7-s, s)]:
            self.grid[corner] = EMPTY
            
        # Add new corners and check if any pieces eliminated as a result
        # (moving counterclockwise starting from top left corner)
        self.numOfShrinks = s = s + 1 
        
        for corner in [(s, s), (s, 7-s), (7-s, 7-s), (7-s, s)]:
            # If corner replaces a piece make sure to eliminate it
            if corner in {**self.get_alive(WHITE), **self.get_alive(BLACK)}:
                self.get_piece(corner).alive = False
                
            # Check eliminations surrounding new corner
            self.grid[corner] = CORNER
            for dir in DIRECTIONS:
                adjacent_square = step(corner, dir)
                if adjacent_square in self.playingarea:
                    if adjacent_square in self.get_alive(WHITE):
                        self.white_pieces[adjacent_square].check_eliminated()
                    elif adjacent_square in self.get_alive(BLACK):
                        self.black_pieces[adjacent_square].check_eliminated()
                    
                
        # Change size of playable area    
        self.playingsize -= 2   
    
    def check_win(self, colour):
        """
        Returns the constant indicating the current result of the board
        for the specified team
        """
        white = 0
        black = 0
        
        # Count the number of alive pieces in each team
        for key, piece in self.white_pieces.items():
            if piece.alive == True:
                white += 1
        for key, piece in self.black_pieces.items():
            if piece.alive == True:
                black += 1
        
        # Check win conditions
        if white >= 2 and black < 2:
            if colour == WHITE:
                return WIN
            else:
                return LOSS
        elif white < 2 and black < 2:
                return TIE
        elif black >= 2 and white < 2:
            if colour == BLACK:
                return  WIN
            else:
                return LOSS
        else:
            return CONTINUE
    
    def print_grid(self):
        """
        Testing purposes only. 
        Prints out physical representation of game board 
        """
        size = range(self.size)
        print('\n'.join(' '.join(self.grid[x,y] for x in size) for y in size))
            
class Piece:
    """
    Class representing each piece in terms of player (WHITE/BLACK), 
    pos (x,y), board (instance of Board it belongs to), alive (whether
    or not it is on the board) and its enemies (WHITE/BLACK)
    """
    def __init__(self, player, pos, board):
        self.player = player
        self.pos = pos
        self.board = board
        self.alive = True
        if player == WHITE:
            self.enemy = [BLACK, CORNER]
        else:
            self.enemy = [WHITE, CORNER]
        
    def listmoves(self, exclude_borders):
        """
        Returns all moves available for this piece. If exclude_borders is true
        only returns moves within the shrink borders
        """
        s = self.board.numOfShrinks
        backup_square = [0,0]
        
        moves = []
        for dir in DIRECTIONS:
            # Try make a normal move
            adjacent_square = step(self.pos, dir)
            if adjacent_square in self.board.playingarea:
                if self.board.grid[adjacent_square] == EMPTY:
                    if exclude_borders == 1 and (adjacent_square[0]==s or \
                                                 adjacent_square[0]==7-s or \
                                                 adjacent_square[1]==s or \
                                                 adjacent_square[1]==7-s):
                        backup_square = adjacent_square
                        continue
                    else:
                        moves.append(adjacent_square)
                        continue # Since jump is not possible
                
            # If not try jump to square next to adjacent square
            jump_square = step(adjacent_square, dir)
            if jump_square in self.board.playingarea:
                if self.board.grid[jump_square] == EMPTY:
                    if exclude_borders == 1 and (jump_square[0]==s or \
                                                 jump_square[0]==7-s or \
                                                 jump_square[1]==s or \
                                                 jump_square[1]==7-s):
                        backup_square = jump_square
                        continue
                    else:
                        moves.append(jump_square)
                        continue
                    
        if len(moves) == 0 and backup_square != [0,0]:
            moves.append(backup_square)
        return moves
    
    def check_eliminated(self):
        """
        Returns true if current piece has been eliminated, removes piece 
        from 'grid' and sets alive = False
        """
        
        # Check if piece is outside of playing area
        if self.pos not in self.board.playingarea:
            self.board.remove_piece(self.pos)
            self.alive = False
            return True
        
        # Check if piece has been surrounded horizontally or vertically
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
        """
        Places piece back on the board and sets alive = True
        """
        self.board.grid[self.pos] = self.player
        self.alive = True
        
    def eliminate_surrounding(self):
        """
        Checks if any adjacent pieces need to be eliminated and return them
        in a list. Only use after moving or placing a piece
        """
        eliminated_pieces = []
        
        if self.player == WHITE:
            enemy_pieces = self.board.black_pieces
        else:
            enemy_pieces = self.board.white_pieces
            
        # Eliminate any surrounding pieces if it is the case
        for dir in DIRECTIONS:
            adjacent_square = step(self.pos, dir)
            if adjacent_square in self.board.playingarea:
                if self.board.grid[adjacent_square] == self.enemy[0]:
                    if enemy_pieces[adjacent_square].check_eliminated():
                        eliminated_pieces.append(enemy_pieces[adjacent_square])
                        
        # Now check if piece has itself been eliminated
        if self.check_eliminated():
            eliminated_pieces.append(self)
                        
        return eliminated_pieces
                    
    def make_move(self, newpos):
        """
        Moves piece to new position and check for eliminations.
        Returns eliminated pieces as a list to enable undomove()
        Assumes given position is valid
        """
        oldpos = self.pos
        self.pos = newpos   
        self.board.grid[oldpos] = EMPTY
        self.board.grid[newpos] = self.player
        self.board.update_team(self.player, newpos, oldpos)
        
        eliminated_pieces = self.eliminate_surrounding()
            
        return eliminated_pieces
        
    def undo_move(self, oldpos, eliminated):
        """
        Move piece back to 'oldpos' and resurrect 'eliminated' pieces
        """
        for piece in eliminated:
            piece.resurrect()
            
        newpos = self.pos
        self.pos = oldpos
        self.board.grid[newpos] = EMPTY
        self.board.grid[oldpos] = self.player
        
        if self.player == WHITE:
            dictionary = self.board.white_pieces
        else:
            dictionary = self.board.black_pieces
        
        # If piece has not been overridden in its team dictionary, update it
        if self.pos in dictionary:
            self.board.update_team(self.player, oldpos, newpos)
        
        # Overridden during alpha beta search so insert into dictionary again   
        else:
            dictionary[oldpos] = self
                 
