#include "chessgame.h"

ChessGame::ChessGame()
{
}

SquareInfo ChessGame::squareInfo(int index)
{
    return _board.squareInfo(index);
}

void ChessGame::move(int src_index, int dst_index)
{
    // 1. validate
    //if (!(_board.getMoves(src_index) & 1 << dst_index))
    //    return;
    // 2. update board
    _board.move(src_index, dst_index);
    // 3. notify
    //emit stateChanged;
}

Bitboard ChessGame::getPossibleMoves(int index)
{
    return _board.getMoves(index);
}
