import array

def bitboard(bitboard, square=None):
	out = ""
	tmp = ""
	for r in range(0, 64):
		row = r / 8 + 1
		col = chr(97 + r % 8)
		if bitboard & (1 << r): tmp += "(%s%d)" % (col, row)
		elif square != None and square == r:  tmp += "[%s%d]" % (col, row)
		else: tmp += " %s%d " % (col, row)
		if col is 'h':
			out = tmp + "\n" + out
			tmp = ""
	print out


def bitboards(bitboards):
	i = 0
	for m in bitboards:
		bitboard(m, i)
		i += 1


def toDecimal(x):
	return sum(map(lambda z: int(x[z]) and 2**(len(x) - z - 1),
	               range(len(x)-1, -1, -1)))


def draw_board(board):
	"""
	+------------------------+
	| R  N  B  Q  K  B  N  R |
	| P  P  P  P  P  P  P  P |
	| .  .  .  .  .  .  .  . |
	| .  .  .  .  .  .  .  . |
	| .  .  .  .  .  .  .  . |
	| .  .  .  .  .  .  .  . |
	| .  .  .  .  .  .  .  . |
	| .  .  .  .  .  .  .  . |
	| p  p  p  p  p  p  p  p |
	| r  n  b  q  k  b  n  r |
	+------------------------+
	"""
	rows = 8
	side = rows*3
	grid = array.array('c', ' '*(rows*side))
	for i in range(64):
		if (1L << i) & board.white_pawns:   grid[i*3] = "p"
		if (1L << i) & board.black_pawns:   grid[i*3] = "P"
		if (1L << i) & board.white_knights: grid[i*3] = "n"
		if (1L << i) & board.black_knights: grid[i*3] = "N"
		if (1L << i) & board.white_bishops: grid[i*3] = "b"
		if (1L << i) & board.black_bishops: grid[i*3] = "B"
		if (1L << i) & board.white_rooks:   grid[i*3] = "r"
		if (1L << i) & board.black_rooks:   grid[i*3] = "R"
		if (1L << i) & board.white_queens:  grid[i*3] = "q"
		if (1L << i) & board.black_queens:  grid[i*3] = "Q"
		if (1L << i) & board.white_king:    grid[i*3] = "k"
		if (1L << i) & board.black_king:    grid[i*3] = "K"
	print "+------------------------+"
	for i in reversed(range(rows)):
		print "|", grid[i*side:(i+1)*side].tostring()[:-2], "|"
	print "+------------------------+"
