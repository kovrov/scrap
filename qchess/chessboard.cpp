#include "chessboard.h"
#include "movebits.h"

ChessBoard::ChessBoard() :
	_white_pawns   (0x000000000000FF00LL),
	_black_pawns   (0x00FF000000000000LL),
	_white_knights (0x0000000000000042LL),
	_black_knights (0x4200000000000000LL),
	_white_bishops (0x0000000000000024LL),
	_black_bishops (0x2400000000000000LL),
	_white_rooks   (0x0000000000000081LL),
	_black_rooks   (0x8100000000000000LL),
	_white_queens  (0x0000000000000008LL),
	_black_queens  (0x0800000000000000LL),
	_white_kings   (0x0000000000000010LL),
	_black_kings   (0x1000000000000000LL),
	moves (0)
{
	_recalc();
}


void ChessBoard::_recalc()
{
	white = _white_pawns | _white_knights | _white_bishops | _white_rooks | _white_queens | _white_kings;
	black = _black_pawns | _black_knights | _black_bishops | _black_rooks | _black_queens | _black_kings;
    occupied = white | black;
	enemy = (moves % 2) == 1 ? white : black;
    //in_check = _in_check();
}

void ChessBoard::move(int src_index, int dst_index)
{
    // TODO: validate!
    moves++;
    _update(1LL << src_index, 1LL << dst_index);
}

void ChessBoard::_update(Bitboard clear_bit, Bitboard set_bit)
{
    // capture
    if (white & set_bit)
    {
		_white_pawns   &= ~set_bit;
		_white_knights &= ~set_bit;
		_white_bishops &= ~set_bit;
		_white_rooks   &= ~set_bit;
		_white_queens  &= ~set_bit;
		_white_kings   &= ~set_bit;
    }
    else if (black & set_bit)
    {
		_black_pawns   &= ~set_bit;
		_black_knights &= ~set_bit;
		_black_bishops &= ~set_bit;
		_black_rooks   &= ~set_bit;
		_black_queens  &= ~set_bit;
		_black_kings   &= ~set_bit;
    }

    // move
	if (_white_pawns & clear_bit)  // a white pawn move...
    {
		_white_pawns ^= clear_bit;
		_white_pawns |= set_bit;
    }
	else if (_black_pawns & clear_bit)  // a black pawn move...
    {
		_black_pawns ^= clear_bit;
		_black_pawns |= set_bit;
    }
	else if (_white_knights & clear_bit)  // a white knight move...
    {
		_white_knights ^= clear_bit;
		_white_knights |= set_bit;
    }
	else if (_black_knights & clear_bit)  // a black knight move...
    {
		_black_knights ^= clear_bit;
		_black_knights |= set_bit;
    }
	else if (_white_bishops & clear_bit)  // a  move...
    {
		_white_bishops ^= clear_bit;
		_white_bishops |= set_bit;
    }
	else if (_black_bishops & clear_bit)  // a  move...
    {
		_black_bishops ^= clear_bit;
		_black_bishops |= set_bit;
    }
	else if (_white_rooks & clear_bit)  // a  move...
    {
		_white_rooks ^= clear_bit;
		_white_rooks |= set_bit;
    }
	else if (_black_rooks & clear_bit)  // a  move...
    {
		_black_rooks ^= clear_bit;
		_black_rooks |= set_bit;
    }
	else if (_white_queens & clear_bit)  // a  move...
    {
		_white_queens ^= clear_bit;
		_white_queens |= set_bit;
    }
	else if (_black_queens & clear_bit)
    {
		_black_queens ^= clear_bit;
		_black_queens |= set_bit;
    }
	else if (_white_kings & clear_bit)
    {
		_white_kings ^= clear_bit;
		_white_kings |= set_bit;
    }
	else if (_black_kings & clear_bit)
    {
		_black_kings ^= clear_bit;
		_black_kings |= set_bit;
    }
    _recalc();
}

Bitboard ChessBoard::getMoves(int index)
{
    Bitboard bit = 1LL << index;
	if (_white_pawns & bit) return _white_pawn_moves(index, ~occupied ^ black);
	if (_black_pawns & bit) return _black_pawn_moves(index, ~occupied ^ white);
	if (_white_knights & bit) return   _knight_moves(index, ~occupied ^ black);
	if (_black_knights & bit) return   _knight_moves(index, ~occupied ^ white);
	if (_white_bishops & bit) return   _bishop_moves(index, ~occupied ^ black);
	if (_black_bishops & bit) return   _bishop_moves(index, ~occupied ^ white);
	if (_white_rooks   & bit) return     _rook_moves(index, ~occupied ^ black);
	if (_black_rooks   & bit) return     _rook_moves(index, ~occupied ^ white);
	if (_white_queens  & bit) return    _queen_moves(index, ~occupied ^ black);
	if (_black_queens  & bit) return    _queen_moves(index, ~occupied ^ white);
	if (_white_kings   & bit) return     _king_moves(index, ~occupied ^ black);
	if (_black_kings   & bit) return     _king_moves(index, ~occupied ^ white);
    return 0LL;
}

Bitboard ChessBoard::_white_pawn_moves(int index, Bitboard enemy_and_empty)
{
    Bitboard pos = 1LL << index;
    Bitboard captures = 0LL;
    Bitboard pawn_moves = pos << 8 & ~occupied;
    if (pawn_moves && index >= 8 && index < 16)
        pawn_moves |= pos << 16 & ~occupied;
    if (index % 8)
        captures = pos << 7;
    if ((index + 1) % 8)
        captures |= pos << 9;
    captures &= enemy_and_empty & occupied;
    // TODO: en passant
    return pawn_moves | captures;
}

Bitboard ChessBoard::_black_pawn_moves(int index, Bitboard enemy_and_empty)
{
    Bitboard pos = 1LL << index;
    Bitboard captures = 0LL;
    Bitboard pawn_moves = pos >> 8 & ~occupied;
    if (pawn_moves && index >= 48 && index < 56)
        pawn_moves |= pos >> 16 & ~occupied;
    if (index % 8)
		captures = pos >> 9;
    if ((index + 1) % 8)
		captures |= pos >> 7;
    captures &= enemy_and_empty & occupied;
	// TODO: en passant
	return pawn_moves | captures;
}

Bitboard ChessBoard::_knight_moves(int index, Bitboard enemy_and_empty)
{
    return knight_moves[index] & enemy_and_empty;
}

Bitboard ChessBoard::_bishop_moves(int index, Bitboard enemy_and_empty)
{
    return _moves_ne(index, enemy_and_empty) |
           _moves_sw(index, enemy_and_empty) |
           _moves_se(index, enemy_and_empty) |
           _moves_nw(index, enemy_and_empty);
}

Bitboard ChessBoard::_rook_moves(int index, Bitboard enemy_and_empty)
{
    return _moves_right(index, enemy_and_empty) |
           _moves_left(index, enemy_and_empty)  |
           _moves_up(index, enemy_and_empty)    |
           _moves_down(index, enemy_and_empty);
}

Bitboard ChessBoard::_queen_moves(int index, Bitboard enemy_and_empty)
{
    return _rook_moves(index, enemy_and_empty) | _bishop_moves(index, enemy_and_empty);
}

Bitboard ChessBoard::_king_moves(int index, Bitboard enemy_and_empty)
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

Bitboard ChessBoard::_moves_right(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = right_moves[index] & occupied;
    Bitboard blocked_slide = blockers<<1 | blockers<<2 | blockers<<3 | blockers<<4 | blockers<<5 | blockers<<6;
    Bitboard blocked_moves = blocked_slide & right_moves[index];
    return ~blocked_moves & (right_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_moves_left(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = left_moves[index] & occupied;
    Bitboard blocked_slide = blockers>>1 | blockers>>2 | blockers>>3 | blockers>>4 | blockers>>5 | blockers>>6;
    Bitboard blocked_moves = blocked_slide & left_moves[index];
    return ~blocked_moves & (left_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_moves_up(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = up_moves[index] & occupied;
    Bitboard blocked_slide = blockers<<8 | blockers<<16 | blockers<<24 | blockers<<32 | blockers<<40 | blockers<<48;
    Bitboard blocked_moves = blocked_slide & up_moves[index];
    return ~blocked_moves & (up_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_moves_down(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = down_moves[index] & occupied;
    Bitboard blocked_slide = blockers>>8 | blockers>>16 | blockers>>24 | blockers>>32 | blockers>>40 | blockers>>48;
    Bitboard blocked_moves = blocked_slide & down_moves[index];
    return ~blocked_moves & (down_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_moves_ne(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = ne_moves[index] & occupied;
    Bitboard blocked_slide = blockers<<9 | blockers<<18 | blockers<<27 | blockers<<36 | blockers<<45 | blockers<<54;
    Bitboard blocked_moves = blocked_slide & ne_moves[index];
    return ~blocked_moves & (ne_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_moves_sw(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = sw_moves[index] & occupied;
    Bitboard blocked_slide = blockers>>9 | blockers>>18 | blockers>>27 | blockers>>36 | blockers>>45 | blockers>>54;
    Bitboard blocked_moves = blocked_slide & sw_moves[index];
    return ~blocked_moves & (sw_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_moves_se(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = se_moves[index] & occupied;
	Bitboard blocked_slide = blockers>>7 | blockers>>14 | blockers>>21 | blockers>>28 | blockers>>35 | blockers>>42;
    Bitboard blocked_moves = blocked_slide & se_moves[index];
    return ~blocked_moves & (se_moves[index] & enemy_and_empty);
}

Bitboard ChessBoard::_moves_nw(int index, Bitboard enemy_and_empty)
{
    Bitboard blockers = nw_moves[index] & occupied;
    Bitboard blocked_slide = blockers<<7 | blockers<<14 | blockers<<21 | blockers<<28 | blockers<<35 | blockers<<42;
    Bitboard blocked_moves = blocked_slide & nw_moves[index];
    return ~blocked_moves & (nw_moves[index] & enemy_and_empty);
}


SquareInfo ChessBoard::squareInfo(int index)
{
    Bitboard bit = 1LL << index;

	if (_white_pawns & bit)
        return SquareInfo(WHITE, PAWN);

	if (_black_pawns & bit)
        return SquareInfo(BLACK, PAWN);

	if (_white_knights & bit)
        return SquareInfo(WHITE, KNIGHT);

	if (_black_knights & bit)
        return SquareInfo(BLACK, KNIGHT);

	if (_white_bishops & bit)
        return SquareInfo(WHITE, BISHOP);

	if (_black_bishops & bit)
        return SquareInfo(BLACK, BISHOP);

	if (_white_rooks & bit)
        return SquareInfo(WHITE, ROOK);

	if (_black_rooks & bit)
        return SquareInfo(BLACK, ROOK);

	if (_white_queens & bit)
        return SquareInfo(WHITE, QUEEN);

	if (_black_queens & bit)
        return SquareInfo(BLACK, QUEEN);

	if (_white_kings & bit)
        return SquareInfo(WHITE, KING);

	if (_black_kings & bit)
        return SquareInfo(BLACK, KING);

    return SquareInfo(COLOR(0), PIECE(0));
}
