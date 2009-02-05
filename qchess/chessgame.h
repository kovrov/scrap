#ifndef CHESSGAME_H
#define CHESSGAME_H

#include <QWidget>
#include "chessboard.h"


enum COLOR { WHITE=1, BLACK };
enum PIECE { PAWN=1, KNIGHT, BISHOP, ROOK, QUEEN, KING };


struct SquareInfo
{
    COLOR color;
    PIECE piece;
    SquareInfo(COLOR c, PIECE p): color(c), piece(p) {}
};


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
    Turn getTurn() { return Turn(moves, (moves % 2) == 0 ? WHITE : BLACK ); }

public slots:
    void move(int src_index, int dst_index);

signals:
    void stateChanged();

private:
    ChessBoard _board;
};


#endif // CHESSGAME_H
