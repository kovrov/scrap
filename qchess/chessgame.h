#ifndef CHESSGAME_H
#define CHESSGAME_H

#include <QWidget>
#include "chessboard.h"


struct Turn
{
    int turn;
    COLOR color;
    Turn(int t, COLOR c) : turn(t), color(c) {}
};


class ChessGame : public QWidget
{
    Q_OBJECT

public:
    ChessGame();
    SquareInfo squareInfo(int index);
    Turn getTurn() { return Turn(_board.getMoveNumber(), (_board.getMoveNumber() % 2) == 0 ? WHITE : BLACK ); }
    Bitboard getPossibleMoves(int index);

public slots:
    void move(int src_index, int dst_index);

signals:
    void stateChanged();

private:
    ChessBoard _board;
};


#endif // CHESSGAME_H
