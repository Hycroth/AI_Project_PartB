from player_module import Player, Board, Piece

white = Player('white')
white.board.place_piece('O', (2,0))
white.board.place_piece('@', (1,0))
white.board.print_board()
white.board.black_pieces[0].check_eliminated()
white.board.print_board()