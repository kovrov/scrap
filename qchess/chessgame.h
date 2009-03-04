#ifndef CHESSGAME_H
#define CHESSGAME_H

#include <QObject>
#include "chessboard.h"


class ChessGame : public QObject
{
	Q_OBJECT

public:
	ChessGame() {}
    PIECE getPiece(int index)  { return _board.getPiece(index); }
	Bitboard getPossibleMoves(int index)  { return _board.getMoves(index); }
    bool isPlayablePiece(int index);
    void move(int src, int dst);
	// game status
	int getMoveNumber() { return _board.getMoveNumber(); }

signals:
	void stateChanged();

private:
    ChessBoard _board;
};


#endif // CHESSGAME_H
