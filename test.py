from player_module import Player, Board, Piece

white = Player('white')

white.board.place_piece('@', (1,0))
white.board.place_piece('@', (2,1))
white.board.place_piece('O', (2,2))
white.board.place_piece('O', (3,2))

white.board.print_grid()
print(white.board.check_win('O'))
print("\n")

white.board.shrink()
white.board.print_grid()
print(white.board.check_win('O'))


