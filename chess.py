import moves
import draw

coords = [
	"a1","b1","c1","d1","e1","f1","g1","h1",
	"a2","b2","c2","d2","e2","f2","g2","h2",
	"a3","b3","c3","d3","e3","f3","g3","h3",
	"a4","b4","c4","d4","e4","f4","g4","h4",
	"a5","b5","c5","d5","e5","f5","g5","h5",
	"a6","b6","c6","d6","e6","f6","g6","h6",
	"a7","b7","c7","d7","e7","f7","g7","h7",
	"a8","b8","c8","d8","e8","f8","g8","h8"]


class Board:
	def __init__(self):
		self.reset()

	def move(self, src, dst):
		src_index = coords.index(src)
		dst_index = coords.index(dst)
		moves_bitboard = self.get_moves(src)
		draw.bitboard(1L << dst_index, src_index)
		if (None == moves_bitboard): moves_bitboard = 0L
		draw.bitboard(moves_bitboard, src_index)
		return
		if moves_bitboard ^ dst_index:
			raise Exception("invalid move")
		if discovered_check :
			raise Exception("discovered check ")
		if in_check:
			raise Exception("king in check")
		uset_bit(src_bitboard, 1L << src_index)
		set_bit(dst_bitboard, 1L << dst_index)

	def get_pieces(self, color, type):
		pass

	def get_piece(self, square):
		index = coords.index(square)
		if (self.white_pawns >> index) & 1:
			return ("white", "pawn", index)
		if (self.black_pawns >> index) & 1:
			return ("black", "pawn", index)
		if (self.white_knights >> index) & 1:
			return ("white", "knight", index)
		if (self.black_knights >> index) & 1:
			return ("black", "knight", index)
		if (self.white_bishops >> index) & 1:
			return ("white", "bishop", index)
		if (self.black_bishops >> index) & 1:
			return ("black", "bishop", index)
		if (self.white_rooks >> index) & 1:
			return ("white", "rook", index)
		if (self.black_rooks >> index) & 1:
			return ("black", "rook", index)
		if (self.white_queens >> index) & 1:
			return ("white", "queen", index)
		if (self.black_queens >> index) & 1:
			return ("black", "queen", index)
		if (self.white_king >> index) & 1:
			return ("white", "king", index)
		if (self.black_king >> index) & 1:
			return ("black", "king", index)

	def reset(self):
		self.white_pawns = 0x000000000000FF00
		self.white_pawns_en_passant = 0x0000000000000000
		#print "white_pawns"
		#draw.bitboard(self.white_pawns)
		self.black_pawns = 0x00FF000000000000
		self.black_pawns_en_passant = 0x0000000000000000
		#print "black_pawns"
		#draw.bitboard(self.black_pawns)
		self.white_knights = 0x0000000000000042
		#print "white_knights"
		#draw.bitboard(self.white_knights)
		self.black_knights = 0x4200000000000000
		#print "black_knights"
		#draw.bitboard(self.black_knights)
		self.white_bishops = 0x0000000000000024
		#print "white_bishops"
		#draw.bitboard(self.white_bishops)
		self.black_bishops = 0x2400000000000000
		#print "black_bishops"
		#draw.bitboard(self.black_bishops)
		self.white_rooks = 0x0000000000000081
		#print "white_rooks"
		#draw.bitboard(self.white_rooks)
		self.black_rooks = 0x8100000000000000
		#print "black_rooks"
		#draw.bitboard(self.black_rooks)
		self.white_queens = 0x0000000000000008
		#print "white_queens"
		#draw.bitboard(self.white_queens)
		self.black_queens = 0x0800000000000000
		#print "black_queens"
		#draw.bitboard(self.black_queens)
		self.white_king = 0x0000000000000010
		#print "white_king"
		#draw.bitboard(self.white_king)
		self.black_king = 0x1000000000000000
		#print "black_king"
		#draw.bitboard(self.black_king)
		self.__recalc_board()

	def __recalc_board(self):
		self.white = self.white_pawns | self.white_knights | \
					self.white_bishops | self.white_rooks | \
					self.white_queens | self.white_king
		self.black = self.black_pawns | self.black_knights | \
					self.black_bishops | self.black_rooks | \
					self.black_queens | self.black_king
		self.occupied = self.white | self.black

	def get_moves(self, square):
		(color, rank, index) = self.get_piece(square)
		if color == "white":
			enemy_and_empty = ~self.occupied ^ self.black
		else:
			enemy_and_empty = ~self.occupied ^ self.white
		if rank == "rook":
			return self.__rook_moves(index, enemy_and_empty)
		elif rank == "bishop":
			return self.__bishop_moves(index, enemy_and_empty)
		elif rank == "queen":
			return self.__queen_moves(index, enemy_and_empty)
		elif rank == "knight":
			return self.__knight_moves(index, enemy_and_empty)
		elif rank == "pawn":
			return self.__pawn_moves(index, enemy_and_empty, (color == "white"))
		elif rank == "king":
			return self.__king_moves(index, enemy_and_empty)


	def __pawn_moves(self, index, enemy_and_empty, up):
		#pawn_captures = moves.pawn_captures[index] & (enemy_and_empty & self.occupied)
		pos = 1L << index
		if up:
			pawn_moves = pos << 8
			if index >= 8 and index < 16:
				pawn_moves |= pos << 16
		else:
			pawn_moves = pos >> 8
			if index >= 48 and index < 56:
				pawn_moves |= pos >> 16

		return pawn_moves #| pawn_captures

	def __knight_moves(self, index, enemy_and_empty):
		return moves.knight[index] & enemy_and_empty

	def __bishop_moves(self, index, enemy_and_empty):
		return self.__moves_ne(index, enemy_and_empty) | \
		       self.__moves_sw(index, enemy_and_empty) | \
		       self.__moves_se(index, enemy_and_empty) | \
		       self.__moves_nw(index, enemy_and_empty)

	def __rook_moves(self, index, enemy_and_empty):
		return self.__moves_right(index, enemy_and_empty) | \
		       self.__moves_left(index, enemy_and_empty) | \
		       self.__moves_up(index, enemy_and_empty) | \
		       self.__moves_down(index, enemy_and_empty)

	def __queen_moves(self, index, enemy_and_empty):
		return self.__rook_moves(index, enemy_and_empty) | self.__bishop_moves(index, enemy_and_empty)

	def __king_moves(self, index, enemy_and_empty):
		return moves.king[index] & enemy_and_empty

	def __moves_right(self, index, enemy_and_empty):
		blockers = moves.right[index] & self.occupied
		blocked_slide = blockers<<1 | blockers<<2 | blockers<<3 | blockers<<4 | blockers<<5 | blockers<<6
		blocked_moves = blocked_slide & moves.right[index]
		return ~blocked_moves & (moves.right[index] & enemy_and_empty)

	def __moves_left(self, index, enemy_and_empty):
		blockers = moves.left[index] & self.occupied
		blocked_slide = blockers>>1 | blockers>>2 | blockers>>3 | blockers>>4 | blockers>>5 | blockers>>6
		blocked_moves = blocked_slide & moves.left[index]
		return ~blocked_moves & (moves.left[index] & enemy_and_empty)

	def __moves_up(self, index, enemy_and_empty):
		blockers = moves.up[index] & self.occupied
		blocked_slide = blockers<<8 | blockers<<16 | blockers<<24 | blockers<<32 | blockers<<40 | blockers<<48
		blocked_moves = blocked_slide & moves.up[index]
		return ~blocked_moves & (moves.up[index] & enemy_and_empty)

	def __moves_down(self, index, enemy_and_empty):
		blockers = moves.down[index] & self.occupied
		blocked_slide = blockers>>8 | blockers>>16 | blockers>>24 | blockers>>32 | blockers>>40 | blockers>>48
		blocked_moves = blocked_slide & moves.down[index]
		return ~blocked_moves & (moves.down[index] & enemy_and_empty)

	def __moves_ne(self, index, enemy_and_empty):
		blockers = moves.ne[index] & self.occupied
		blocked_slide = blockers<<9 | blockers<<18 | blockers<<27 | blockers<<36 | blockers<<45 | blockers<<54
		blocked_moves = blocked_slide & moves.ne[index]
		return ~blocked_moves & (moves.ne[index] & enemy_and_empty)

	def __moves_sw(self, index, enemy_and_empty):
		blockers = moves.sw[index] & self.occupied
		blocked_slide = blockers>>9 | blockers>>18 | blockers>>27 | blockers>>36 | blockers>>45 | blockers>>54
		blocked_moves = blocked_slide & moves.sw[index]
		return ~blocked_moves & (moves.sw[index] & enemy_and_empty)

	def __moves_se(self, index, enemy_and_empty):
		blockers = moves.se[index] & self.occupied
		blocked_slide = blockers<<7 | blockers<<14 | blockers<<21 | blockers<<28 | blockers<<35 | blockers<<42
		blocked_moves = blocked_slide & moves.se[index]
		return ~blocked_moves & (moves.se[index] & enemy_and_empty)

	def __moves_nw(self, index, enemy_and_empty):
		blockers = moves.nw[index] & self.occupied
		blocked_slide = blockers<<7 | blockers<<14 | blockers<<21 | blockers<<28 | blockers<<35 | blockers<<42
		blocked_moves = blocked_slide & moves.nw[index]
		return ~blocked_moves & (moves.nw[index] & enemy_and_empty)


def test():
	#draw.bitboards(moves.pawn_captures)
	#draw.bitboards(moves.right)
	#draw.bitboards(moves.up)
	#draw.bitboards(moves.down)
	#draw.bitboards(moves.ne)
	#draw.bitboards(moves.nw)
	#draw.bitboards(moves.sw)
	#draw.bitboards(moves.se)
	#draw.bitboards(moves.knight)
	
	board = Board() # new game, white turn
	# move white pawn e2 - e4
	board.move("e2", "e4")
	# move black pawn e7 - e5
	board.move("e7", "e5")
	# error exampes
	board.get_moves("e7") # e7 empty - throw
	# queen
	board.move("d1", "d5") # invalid move - throw
	# etc...

if __name__ == '__main__':
	test()
