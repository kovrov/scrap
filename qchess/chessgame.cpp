#include "chessgame.h"

ChessGame::ChessGame()
{
}

SquareInfo ChessGame::squareInfo(int index)
{
    Bitboard bit = 1LL << index;
    if (_board.white_pawns & bit)
    {
        return SquareInfo(WHITE, PAWN);
    }
    if (_board.black_pawns & bit)
    {
        return SquareInfo(BLACK, PAWN);
    }
    if (_board.white_knights & bit)
    {
        return SquareInfo(WHITE, KNIGHT);
    }
    if (_board.black_knights & bit)
    {
        return SquareInfo(BLACK, KNIGHT);
    }
    if (_board.white_bishops & bit)
    {
        return SquareInfo(WHITE, BISHOP);
    }
    if (_board.black_bishops & bit)
    {
        return SquareInfo(BLACK, BISHOP);
    }
    if (_board.white_rooks & bit)
    {
        return SquareInfo(WHITE, ROOK);
    }
    if (_board.black_rooks & bit)
    {
        return SquareInfo(BLACK, ROOK);
    }
    if (_board.white_queens & bit)
    {
        return SquareInfo(WHITE, QUEEN);
    }
    if (_board.black_queens & bit)
    {
        return SquareInfo(BLACK, QUEEN);
    }
    if (_board.white_kings & bit)
    {
        return SquareInfo(WHITE, KING);
    }
    if (_board.black_kings & bit)
    {
        return SquareInfo(BLACK, KING);
    }
    return SquareInfo(COLOR(0), PIECE(0));
}
