#ifndef CHESSBOARD_H
#define CHESSBOARD_H


typedef unsigned long long Bitboard;  // 64-bit

enum COLOR { WHITE=1, BLACK };
enum PIECE { PAWN=1, KNIGHT, BISHOP, ROOK, QUEEN, KING };

struct SquareInfo
{
    COLOR color;
    PIECE piece;
    SquareInfo(COLOR c, PIECE p): color(c), piece(p) {}
};


class ChessBoard
{
public:
    ChessBoard();
	Bitboard getMoves(int index);
    int getMoveNumber() { return moves; }
    void move(int src_index, int dst_index);
    SquareInfo squareInfo(int index);

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
    void _update(Bitboard clear_bit, Bitboard set_bit);
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
