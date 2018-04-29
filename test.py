from player_module import Player, Board, Piece

white = Player('white')
white.board.place_piece(white.colour, (1,0))
white.board.print_board()