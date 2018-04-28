# Piece module for COMP30024: Artificial Intelligence, 2018
# Authors: Ckyever Gaviola, Samuel Fatone
# Note: Some ideas have been borrowed from the sample-solution

import numpy

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
    def __init__(self):
        # Initialise default size board (8x8)
        self.b = [[EMPTY for x in range(8)] for y in range(8)]
        for corner in [(0,0), (0,7), (7,0), (7,7)]:
            cy, cx = corner
            self.b[cy][cx] = CORNER
        
    def print(self):
        # For testing only. Prints out the gameboard
        print(numpy.matrix(self.b))
        
class Piece:
    def __init__(self, player, pos, board):
        self.player = player
        self.pos = pos
        self.board = board
        self.alive = True