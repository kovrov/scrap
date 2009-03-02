#ifndef CHESSGAME_H
#define CHESSGAME_H

#include <QObject>
#include "chessboard.h"


struct Turn
{
    int turn;
    COLOR color;
    Turn(int t, COLOR c) : turn(t), color(c) {}
};


class ChessGame : public QObject
{
    Q_OBJECT

public:
	ChessGame() {}
	SquareInfo squareInfo(int index)  { return _board.squareInfo(index); }
	Turn getTurn()  { return Turn(_board.getMoveNumber(), (_board.getMoveNumber() % 2) == 0 ? WHITE : BLACK); }
	Bitboard getPossibleMoves(int index)  { return _board.getMoves(index); }

public slots:
	void move(int src, int dst);

signals:
    void stateChanged();

private:
    ChessBoard _board;
};


#endif // CHESSGAME_H
