from player_module import Player, Board, Piece

white = Player('white')
white.board.place_piece('O', (3,0))
white.board.place_piece('@', (1,0))
white.board.print_board()
print('\n')

white.board.white_pieces[(3,0)].make_move((2,0))
white.board.print_board()