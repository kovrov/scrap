#include "chessboard.h"
#include "movebits.h"

ChessBoard::ChessBoard() :
    white_pawns (0x000000000000FF00LL),
    black_pawns (0x00FF000000000000LL),
    white_knights (0x0000000000000042LL),
    black_knights (0x4200000000000000LL),
    white_bishops (0x0000000000000024LL),
    black_bishops (0x2400000000000000LL),
    white_rooks (0x0000000000000081LL),
    black_rooks (0x8100000000000000LL),
    white_queens (0x0000000000000008LL),
    black_queens (0x0800000000000000LL),
    white_king (0x0000000000000010LL),
    black_king (0x1000000000000000LL),
    turn (0)
{
}


void ChessBoard::_recalc()
{
    white = white_pawns | white_knights | white_bishops | white_rooks | white_queens | white_king;
    black = black_pawns | black_knights | black_bishops | black_rooks | black_queens | black_king;
    occupied = white | black;
    enemy = (turn % 2) ? white : black;
    //in_check = __in_check();
}

void ChessBoard::move(int src_index, int dst_index)
{
    Bitboard src_bit = 1L << src_index;
    Bitboard dst_bit = 1L << dst_index;
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
    else if (white_king & src_bit)
    {
        white_king ^= src_bit;
        white_king |= dst_bit;
    }
    else if (black_king & src_bit)
    {
        black_king ^= src_bit;
        black_king |= dst_bit;
    }
    //else
    //    raise Exception("invalid move");
    turn++;
    _recalc();
}
