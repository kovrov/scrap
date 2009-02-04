#ifndef CHESSBOARD_H
#define CHESSBOARD_H

#include <QWidget>
#include "squareinfo.h"

typedef unsigned long long Bitboard;
class SquareInfo;
struct Turn
{
	int turn;
	COLOR color;
	Turn(int t, COLOR c) : turn(t), color(c) {}
};

class ChessBoard : public QWidget
{
	Q_OBJECT

public:
    ChessBoard();
    SquareInfo squareInfo(int index);
	Turn getTurn();
	Bitboard getMoves(int index);

public slots:
	void move(int src_index, int dst_index);

signals:
	void stateChanged();

private:
    Bitboard white_pawns,
             black_pawns,
             white_knights,
             black_knights,
             white_bishops,
             black_bishops,
             white_rooks,
             black_rooks,
             white_queens,
             black_queens,
             white_kings,
             black_kings;
    Bitboard white, black, occupied, enemy;
	int moves;
    void _recalc();
    Bitboard _white_pawn_moves(int index, Bitboard enemy_and_empty);
    Bitboard _black_pawn_moves(int index, Bitboard enemy_and_empty);
    Bitboard _knight_moves(int index, Bitboard enemy_and_empty);
    Bitboard _bishop_moves(int index, Bitboard enemy_and_empty);
    Bitboard _rook_moves(int index, Bitboard enemy_and_empty);
    Bitboard _queen_moves(int index, Bitboard enemy_and_empty);
    Bitboard _king_moves(int index, Bitboard enemy_and_empty);
    Bitboard _moves_right(int index, Bitboard enemy_and_empty);
    Bitboard _moves_left(int index, Bitboard enemy_and_empty);
    Bitboard _moves_up(int index, Bitboard enemy_and_empty);
    Bitboard _moves_down(int index, Bitboard enemy_and_empty);
    Bitboard _moves_ne(int index, Bitboard enemy_and_empty);
    Bitboard _moves_sw(int index, Bitboard enemy_and_empty);
    Bitboard _moves_se(int index, Bitboard enemy_and_empty);
    Bitboard _moves_nw(int index, Bitboard enemy_and_empty);
};

#endif // CHESSBOARD_H
