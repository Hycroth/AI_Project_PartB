# Player module for COMP30024: Artificial Intelligence, 2018
# Authors: Ckyever Gaviola, Samuel Fatone

from watchyourback import Board, Piece

class Player:
    def __init__(self, colour):
        if colour == 'white':
            self.colour = 'O'
        if colour == 'black':
            self.colour = '@'
        self.board = Board()
        
    ## Returns next move
    def action(self, turns):
        
        return next_action
    
    ## Update game board with opponents move
    def update(self, action):
        
        return