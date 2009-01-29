#ifndef CHESSBOARD_H
#define CHESSBOARD_H

typedef unsigned long long Bitboard;

class ChessBoard
{
public:
    ChessBoard();
    void move(int src_index, int dst_index);
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
             white_king,
             black_king;
    Bitboard white, black, occupied, enemy;
    int turn;
    void _recalc();

};

#endif // CHESSBOARD_H
