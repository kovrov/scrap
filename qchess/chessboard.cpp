#include "chessboard.h"
#include "movebits.h"
#include "squareinfo.h"

ChessBoard::ChessBoard() :
	white_pawns   (0x000000000000FF00LL),
	black_pawns   (0x00FF000000000000LL),
    white_knights (0x0000000000000042LL),
    black_knights (0x4200000000000000LL),
    white_bishops (0x0000000000000024LL),
    black_bishops (0x2400000000000000LL),
	white_rooks   (0x0000000000000081LL),
	black_rooks   (0x8100000000000000LL),
	white_queens  (0x0000000000000008LL),
	black_queens  (0x0800000000000000LL),
	white_kings   (0x0000000000000010LL),
	black_kings   (0x1000000000000000LL),
    turn (0)
{
}


void ChessBoard::_recalc()
{
    white = white_pawns | white_knights | white_bishops | white_rooks | white_queens | white_kings;
    black = black_pawns | black_knights | black_bishops | black_rooks | black_queens | black_kings;
    occupied = white | black;
    enemy = (turn % 2) ? white : black;
    //in_check = _in_check();
}

void ChessBoard::move(int src_index, int dst_index)
{
    Bitboard src_bit = 1LL << src_index;
    Bitboard dst_bit = 1LL << dst_index;
    if (white_pawns & src_bit)
    {
        white_pawns ^= src_bit;
        white_pawns |= dst_bit;
    }
    else if (black_pawns & src_bit)
    {
        black_pawns ^= src_bit;
        black_pawns |= dst_bit;
    }
    else if (white_knights & src_bit)
    {
        white_knights ^= src_bit;
        white_knights |= dst_bit;
    }
    else if (black_knights & src_bit)
    {
        black_knights ^= src_bit;
        black_knights |= dst_bit;
    }
    else if (white_bishops & src_bit)
    {
        white_bishops ^= src_bit;
        white_bishops |= dst_bit;
    }
    else if (black_bishops & src_bit)
    {
        black_bishops ^= src_bit;
        black_bishops |= dst_bit;
    }
    else if (white_rooks & src_bit)
    {
        white_rooks ^= src_bit;
        white_rooks |= dst_bit;
    }
    else if (black_rooks & src_bit)
    {
        black_rooks ^= src_bit;
        black_rooks |= dst_bit;
    }
    else if (white_queens & src_bit)
    {
        white_queens ^= src_bit;
        white_queens |= dst_bit;
    }
    else if (black_queens & src_bit)
    {
        black_queens ^= src_bit;
        black_queens |= dst_bit;
    }
    else if (white_kings & src_bit)
    {
        white_kings ^= src_bit;
        white_kings |= dst_bit;
    }
    else if (black_kings & src_bit)
    {
        black_kings ^= src_bit;
        black_kings |= dst_bit;
    }
    //else
    //    raise Exception("invalid move");
    turn++;
    _recalc();
}

SquareInfo ChessBoard::squareInfo(int index)
{
    Bitboard bit = 1LL << index;
    if (white_pawns & bit)
    {
        return SquareInfo(WHITE, PAWN);
    }
    if (black_pawns & bit)
    {
        return SquareInfo(BLACK, PAWN);
    }
    if (white_knights & bit)
    {
        return SquareInfo(WHITE, KNIGHT);
    }
    if (black_knights & bit)
    {
        return SquareInfo(BLACK, KNIGHT);
    }
    if (white_bishops & bit)
    {
        return SquareInfo(WHITE, BISHOP);
    }
    if (black_bishops & bit)
    {
        return SquareInfo(BLACK, BISHOP);
    }
    if (white_rooks & bit)
    {
        return SquareInfo(WHITE, ROOK);
    }
    if (black_rooks & bit)
    {
        return SquareInfo(BLACK, ROOK);
    }
    if (white_queens & bit)
    {
        return SquareInfo(WHITE, QUEEN);
    }
    if (black_queens & bit)
    {
        return SquareInfo(BLACK, QUEEN);
    }
    if (white_kings & bit)
    {
        return SquareInfo(WHITE, KING);
    }
    if (black_kings & bit)
    {
        return SquareInfo(BLACK, KING);
    }
    return SquareInfo(COLOR(0), PIECE(0));
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
        captures = pos >> 7;
    if ((index + 1) % 8)
        captures |= pos >> 9;
    captures &= enemy_and_empty & occupied;
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
    Bitboard blocked_slide = blockers<<7 | blockers<<14 | blockers<<21 | blockers<<28 | blockers<<35 | blockers<<42;
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
