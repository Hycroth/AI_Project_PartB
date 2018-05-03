from player_module import Player, Board, Piece

white = Player('white')
white.board.place_piece('O', (0,1))
white.board.place_piece('@', (1,1))
white.board.place_piece('@', (3,1))
white.board.place_piece('O', (4,1))
white.board.place_piece('@', (2,2))
white.board.place_piece('O', (2,3))
white.board.print_grid()
print('\n')

elim = white.board.place_piece('O', (2,1))
white.board.print_grid()
print('\n')

white.board.undo_place('O', (2,1), elim)
white.board.print_grid()
print('\n')