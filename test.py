from minimax_module import Player, Board, Piece

white = Player('white')
black = Player('black')

white.board.place_piece('@', (1,2))
white.board.place_piece('@', (3,2))
eliminated = white.board.place_piece('O', (2,1))
white.board.print_grid()
print(white.board.white_pieces)

print("\n")

eliminated = white.board.white_pieces[(2,1)].make_move((2,2))
white.board.print_grid()
print(white.board.white_pieces)

print("\n")

white.board.white_pieces[(2,2)].undo_move((2,1), eliminated)
white.board.print_grid()
print(white.board.white_pieces)

