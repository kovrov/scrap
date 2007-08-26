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
