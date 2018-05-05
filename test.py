from player_module import Player, Board, Piece

white = Player('white')
black = Player('black')

white.board.place_piece('O', (1,0))
white.board.place_piece('@', (1,2))
white.board.place_piece('@', (2,2))

white.board.print_grid()
print(white.board.get_alive('O'))
print(white.board.get_alive('@'))

white.board.place_piece('@', (2,0))

white.board.print_grid()
print(white.board.get_alive('O'))
print(white.board.get_alive('@'))
