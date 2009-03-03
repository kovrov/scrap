#ifndef CHESSGAME_H
#define CHESSGAME_H

#include "chessboard.h"


class ChessGame
{
public:
	ChessGame() {}
    PIECE getPiece(int index)  { return _board.getPiece(index); }
	Bitboard getPossibleMoves(int index)  { return _board.getMoves(index); }
    bool isPlayablePiece(int index)
    {
        if (_board.getMoveNumber() % 2 == 0)  // WHITE
            return _board.isPieceWhite(index);
        else  // BLACK
            return _board.isPieceBlack(index);
    }
    void move(int src, int dst);

private:
    ChessBoard _board;
};


#endif // CHESSGAME_H
