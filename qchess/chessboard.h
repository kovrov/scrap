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
