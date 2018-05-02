from player_module import Player, Board, Piece

white = Player('white')
white.board.place_piece('O', (2,0))
white.board.place_piece('O', (0,1))
white.board.place_piece('@', (1,1))
white.board.place_piece('@', (3,1))
white.board.place_piece('O', (4,1))
white.board.place_piece('@', (2,2))
white.board.place_piece('O', (2,3))
white.board.print_board()
print('\n')

eliminated = white.board.white_pieces[(2,0)].make_move((2,1))
white.board.print_board()
print('\n')

white.board.white_pieces[(2,1)].undo_move((2,0), eliminated)
white.board.print_board()
print('\n')