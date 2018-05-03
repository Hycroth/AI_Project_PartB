from player_module import Player, Board, Piece

white = Player('white')

white.board.place_piece('@', (1,0))
white.board.place_piece('@', (6,0))
white.board.place_piece('@', (2,1))
white.board.place_piece('O', (3,1))
white.board.place_piece('O', (4,1))
white.board.place_piece('@', (5,1))
white.board.place_piece('@', (0,2))
white.board.place_piece('@', (7,2))

white.board.place_piece('@', (1,7))
white.board.place_piece('@', (6,7))
white.board.place_piece('@', (2,6))
white.board.place_piece('O', (3,6))
white.board.place_piece('O', (4,6))
white.board.place_piece('@', (5,6))
white.board.place_piece('@', (0,5))
white.board.place_piece('@', (7,5))

white.board.print_grid()
print("\n")

white.board.shrink()
white.board.print_grid()


