#include "chessboard.h"
#include "movebits.h"

ChessBoard::ChessBoard() :
	_whitePawns   (0x000000000000FF00LL),
	_blackPawns   (0x00FF000000000000LL),
	_whiteKnights (0x0000000000000042LL),
	_blackKnights (0x4200000000000000LL),
	_whiteBishops (0x0000000000000024LL),
	_blackBishops (0x2400000000000000LL),
	_whiteRooks   (0x0000000000000081LL),
	_blackRooks   (0x8100000000000000LL),
	_whiteQueens  (0x0000000000000008LL),
	_blackQueens  (0x0800000000000000LL),
	_whiteKings   (0x0000000000000010LL),
	_blackKings   (0x1000000000000000LL),
	_moves (0)
{
	_recalc();
}


void ChessBoard::_recalc()
{
    _whitePieces = _whitePawns | _whiteKnights | _whiteBishops | _whiteRooks | _whiteQueens | _whiteKings;
    _blackPieces = _blackPawns | _blackKnights | _blackBishops | _blackRooks | _blackQueens | _blackKings;
    _occupiedSquares = _whitePieces | _blackPieces;
    //_enemy = (_moves % 2) == 1 ? _whitePieces : _blackPieces;
    //in_check = _in_check();
}

void ChessBoard::move(int src_index, int dst_index)
{
    // TODO: validate!
	Bitboard src_bit = 1LL << src_index;
	Bitboard dst_bit = 1LL << dst_index;

	// capture
    if (_whitePieces & dst_bit)
	{
		_whitePawns   &= ~dst_bit;
		_whiteKnights &= ~dst_bit;
		_whiteBishops &= ~dst_bit;
		_whiteRooks   &= ~dst_bit;
		_whiteQueens  &= ~dst_bit;
		_whiteKings   &= ~dst_bit;
	}
    else if (_blackPieces & dst_bit)
	{
		_blackPawns   &= ~dst_bit;
		_blackKnights &= ~dst_bit;
		_blackBishops &= ~dst_bit;
		_blackRooks   &= ~dst_bit;
		_blackQueens  &= ~dst_bit;
		_blackKings   &= ~dst_bit;
	}

	// move
	if (_whitePawns & src_bit)  // a white pawn move...
	{
		_whitePawns ^= src_bit;
		_whitePawns |= dst_bit;
	}
	else if (_blackPawns & src_bit)  // a black pawn move...
	{
		_blackPawns ^= src_bit;
		_blackPawns |= dst_bit;
	}
	else if (_whiteKnights & src_bit)  // a white knight move...
	{
		_whiteKnights ^= src_bit;
		_whiteKnights |= dst_bit;
	}
	else if (_blackKnights & src_bit)  // a black knight move...
	{
		_blackKnights ^= src_bit;
		_blackKnights |= dst_bit;
	}
	else if (_whiteBishops & src_bit)  // a  move...
	{
		_whiteBishops ^= src_bit;
		_whiteBishops |= dst_bit;
	}
	else if (_blackBishops & src_bit)  // a  move...
	{
		_blackBishops ^= src_bit;
		_blackBishops |= dst_bit;
	}
	else if (_whiteRooks & src_bit)  // a  move...
	{
		_whiteRooks ^= src_bit;
		_whiteRooks |= dst_bit;
	}
	else if (_blackRooks & src_bit)  // a  move...
	{
		_blackRooks ^= src_bit;
		_blackRooks |= dst_bit;
	}
	else if (_whiteQueens & src_bit)  // a  move...
	{
		_whiteQueens ^= src_bit;
		_whiteQueens |= dst_bit;
	}
	else if (_blackQueens & src_bit)
	{
		_blackQueens ^= src_bit;
		_blackQueens |= dst_bit;
	}
	else if (_whiteKings & src_bit)
	{
		_whiteKings ^= src_bit;
		_whiteKings |= dst_bit;
	}
	else if (_blackKings & src_bit)
	{
		_blackKings ^= src_bit;
		_blackKings |= dst_bit;
	}

	_moves++;
	_recalc();
}

Bitboard ChessBoard::getMoves(int index)
{
    Bitboard bit = 1LL << index;
    if (_whitePawns & bit) return _whitePawnMoves(index, ~_occupiedSquares ^ _blackPieces);
    if (_blackPawns & bit) return _blackPawnMoves(index, ~_occupiedSquares ^ _whitePieces);
    if (_whiteKnights & bit) return  _knightMoves(index, ~_occupiedSquares ^ _blackPieces);
    if (_blackKnights & bit) return  _knightMoves(index, ~_occupiedSquares ^ _whitePieces);
    if (_whiteBishops & bit) return  _bishopMoves(index, ~_occupiedSquares ^ _blackPieces);
    if (_blackBishops & bit) return  _bishopMoves(index, ~_occupiedSquares ^ _whitePieces);
    if (_whiteRooks   & bit) return    _rookMoves(index, ~_occupiedSquares ^ _blackPieces);
    if (_blackRooks   & bit) return    _rookMoves(index, ~_occupiedSquares ^ _whitePieces);
    if (_whiteQueens  & bit) return   _queenMoves(index, ~_occupiedSquares ^ _blackPieces);
    if (_blackQueens  & bit) return   _queenMoves(index, ~_occupiedSquares ^ _whitePieces);
    if (_whiteKings   & bit) return    _kingMoves(index, ~_occupiedSquares ^ _blackPieces);
    if (_blackKings   & bit) return    _kingMoves(index, ~_occupiedSquares ^ _whitePieces);
    return 0LL;
}

Bitboard ChessBoard::_whitePawnMoves(int index, Bitboard enemy_and_empty)
{
    Bitboard pos = 1LL << index;
    Bitboard captures = 0LL;
    Bitboard pawn_moves = pos << 8 & ~_occupiedSquares;
    if (pawn_moves && index >= 8 && index < 16)
        pawn_moves |= pos << 16 & ~_occupiedSquares;
    if (index % 8)
        captures = pos << 7;
    if ((index + 1) % 8)
        captures |= pos << 9;
    captures &= enemy_and_empty & _occupiedSquares;
    // TODO: en passant
    return pawn_moves | captures;
}

Bitboard ChessBoard::_blackPawnMoves(int index, Bitboard enemy_and_empty)
{
    Bitboard pos = 1LL << index;
    Bitboard captures = 0LL;
    Bitboard pawn_moves = pos >> 8 & ~_occupiedSquares;
    if (pawn_moves && index >= 48 && index < 56)
        pawn_moves |= pos >> 16 & ~_occupiedSquares;
    if (index % 8)
		captures = pos >> 9;
    if ((index + 1) % 8)
		captures |= pos >> 7;
    captures &= enemy_and_empty & _occupiedSquares;
	// TODO: en passant
	return pawn_moves | captures;
}

Bitboard ChessBoard::_knightMoves(int index, Bitboard enemy_and_empty)
{
    return knight_moves[index] & enemy_and_empty;
}

Bitboard ChessBoard::_bishopMoves(int index, Bitboard enemy_and_empty)
{
	return _neMoves(index, enemy_and_empty) |
		   _swMoves(index, enemy_and_empty) |
		   _seMoves(index, enemy_and_empty) |
		   _nwMoves(index, enemy_and_empty);
}

Bitboard ChessBoard::_rookMoves(int index, Bitboard enemy_and_empty)
{
	return _rightMoves(index, enemy_and_empty) |
		   _leftMoves(index, enemy_and_empty)  |
		   _upMoves(index, enemy_and_empty)    |
		   _downMoves(index, enemy_and_empty);
}

Bitboard ChessBoard::_queenMoves(int index, Bitboard enemy_and_empty)
{
	return _rookMoves(index, enemy_and_empty) | _bishopMoves(index, enemy_and_empty);
}

Bitboard ChessBoard::_kingMoves(int index, Bitboard enemy_and_empty)
{
    Bitboard pos = 1LL << index;
    Bitboard king_moves = pos << 8 | pos >> 8;
    if (index % 8)
        king_moves |= pos << 7 | pos >> 9;
        king_moves |= pos >> 1;
    if ((index + 1) % 8)
        king_moves |= pos << 9 | pos >> 7;
        king_moves |= pos << 1;
    // TODO: castling
    return king_moves & enemy_and_empty;
}

Bitboard ChessBoard::_rightMoves(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = right_moves[index] & _occupiedSquares;
    Bitboard blocked_slide = blockers<<1 | blockers<<2 | blockers<<3 | blockers<<4 | blockers<<5 | blockers<<6;
    Bitboard blocked_moves = blocked_slide & right_moves[index];
    return ~blocked_moves & (right_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_leftMoves(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = left_moves[index] & _occupiedSquares;
    Bitboard blocked_slide = blockers>>1 | blockers>>2 | blockers>>3 | blockers>>4 | blockers>>5 | blockers>>6;
    Bitboard blocked_moves = blocked_slide & left_moves[index];
    return ~blocked_moves & (left_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_upMoves(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = up_moves[index] & _occupiedSquares;
    Bitboard blocked_slide = blockers<<8 | blockers<<16 | blockers<<24 | blockers<<32 | blockers<<40 | blockers<<48;
    Bitboard blocked_moves = blocked_slide & up_moves[index];
    return ~blocked_moves & (up_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_downMoves(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = down_moves[index] & _occupiedSquares;
    Bitboard blocked_slide = blockers>>8 | blockers>>16 | blockers>>24 | blockers>>32 | blockers>>40 | blockers>>48;
    Bitboard blocked_moves = blocked_slide & down_moves[index];
    return ~blocked_moves & (down_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_neMoves(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = ne_moves[index] & _occupiedSquares;
    Bitboard blocked_slide = blockers<<9 | blockers<<18 | blockers<<27 | blockers<<36 | blockers<<45 | blockers<<54;
    Bitboard blocked_moves = blocked_slide & ne_moves[index];
    return ~blocked_moves & (ne_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_swMoves(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = sw_moves[index] & _occupiedSquares;
    Bitboard blocked_slide = blockers>>9 | blockers>>18 | blockers>>27 | blockers>>36 | blockers>>45 | blockers>>54;
    Bitboard blocked_moves = blocked_slide & sw_moves[index];
    return ~blocked_moves & (sw_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_seMoves(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = se_moves[index] & _occupiedSquares;
	Bitboard blocked_slide = blockers>>7 | blockers>>14 | blockers>>21 | blockers>>28 | blockers>>35 | blockers>>42;
    Bitboard blocked_moves = blocked_slide & se_moves[index];
    return ~blocked_moves & (se_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_nwMoves(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = nw_moves[index] & _occupiedSquares;
    Bitboard blocked_slide = blockers<<7 | blockers<<14 | blockers<<21 | blockers<<28 | blockers<<35 | blockers<<42;
    Bitboard blocked_moves = blocked_slide & nw_moves[index];
    return ~blocked_moves & (nw_moves[index] & enemy_and_empty);
}


PIECE ChessBoard::getPiece(int index)
{
    Bitboard bit = 1LL << index;

	if (_whitePawns & bit)
        return WHITE_PAWN;

	if (_blackPawns & bit)
        return BLACK_PAWN;

	if (_whiteKnights & bit)
        return WHITE_KNIGHT;

	if (_blackKnights & bit)
        return BLACK_KNIGHT;

	if (_whiteBishops & bit)
        return WHITE_BISHOP;

	if (_blackBishops & bit)
        return BLACK_BISHOP;

	if (_whiteRooks & bit)
        return WHITE_ROOK;

	if (_blackRooks & bit)
        return BLACK_ROOK;

	if (_whiteQueens & bit)
        return WHITE_QUEEN;

	if (_blackQueens & bit)
        return BLACK_QUEEN;

	if (_whiteKings & bit)
        return WHITE_KING;

	if (_blackKings & bit)
        return BLACK_KING;

    return NONE;
}
