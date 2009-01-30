#include "squareinfo.h"

SquareInfo::SquareInfo(COLOR c, PIECE p) :
    color (c),
    piece (p)
{
    if (color == WHITE)
    {
        str =   piece == PAWN ? "wp" :
                piece == KNIGHT ? "wn" :
                piece == BISHOP ? "wb" :
                piece == ROOK ? "wr" :
                piece == QUEEN ? "wq" :
                piece == KING ? "wk" :
                "";
    }
    else if (color == BLACK)
    {
        str =   piece == PAWN ? "bp" :
                piece == KNIGHT ? "bn" :
                piece == BISHOP ? "bb" :
                piece == ROOK ? "br" :
                piece == QUEEN ? "bq" :
                piece == KING ? "bk" :
                "";
    }
    else
        str = "";
}
