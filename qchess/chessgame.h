#ifndef CHESSGAME_H
#define CHESSGAME_H

#include "chessboard.h"


struct Turn
{
    int turn;
    COLOR color;
    Turn(int t, COLOR c) : turn(t), color(c) {}
};


class ChessGame
{
public:
	ChessGame() {}
	SquareInfo getSquareInfo(int index)  { return _board.getSquareInfo(index); }
	Turn getTurn()  { return Turn(_board.getMoveNumber(), (_board.getMoveNumber() % 2) == 0 ? WHITE : BLACK); }
	Bitboard getPossibleMoves(int index)  { return _board.getMoves(index); }
	void move(int src, int dst);

private:
    ChessBoard _board;
};


#endif // CHESSGAME_H
