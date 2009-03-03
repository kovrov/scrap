#ifndef CHESSBOARD_H
#define CHESSBOARD_H


typedef unsigned long long Bitboard;  // 64-bit

enum PIECE { NONE = -1,
             WHITE_PAWN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_ROOK, WHITE_QUEEN, WHITE_KING,
             BLACK_PAWN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_ROOK, BLACK_QUEEN, BLACK_KING };


class ChessBoard
{
public:
    ChessBoard();
	Bitboard getMoves(int index);
	int getMoveNumber() { return _moves; }
    void move(int src_index, int dst_index);
    PIECE getPiece(int index);
    bool isPieceWhite(int index) { return (_whitePieces & 1LL << index) ? true : false; }
    bool isPieceBlack(int index) { return (_blackPieces & 1LL << index) ? true : false; }

private:
	Bitboard _whitePawns,
			 _blackPawns,
			 _whiteKnights,
			 _blackKnights,
			 _whiteBishops,
			 _blackBishops,
			 _whiteRooks,
			 _blackRooks,
			 _whiteQueens,
			 _blackQueens,
			 _whiteKings,
			 _blackKings;
    Bitboard _whitePieces, _blackPieces, _occupiedSquares;//, _enemy;
	int _moves;
    void _recalc();
	Bitboard _whitePawnMoves(int index, Bitboard enemy_and_empty);
	Bitboard _blackPawnMoves(int index, Bitboard enemy_and_empty);
	Bitboard _knightMoves(   int index, Bitboard enemy_and_empty);
	Bitboard _bishopMoves(   int index, Bitboard enemy_and_empty);
	Bitboard _rookMoves(     int index, Bitboard enemy_and_empty);
	Bitboard _queenMoves(    int index, Bitboard enemy_and_empty);
	Bitboard _kingMoves(     int index, Bitboard enemy_and_empty);
	Bitboard _rightMoves(    int index, Bitboard enemy_and_empty);
	Bitboard _leftMoves(     int index, Bitboard enemy_and_empty);
	Bitboard _upMoves(       int index, Bitboard enemy_and_empty);
	Bitboard _downMoves(     int index, Bitboard enemy_and_empty);
	Bitboard _neMoves(       int index, Bitboard enemy_and_empty);
	Bitboard _swMoves(       int index, Bitboard enemy_and_empty);
	Bitboard _seMoves(       int index, Bitboard enemy_and_empty);
	Bitboard _nwMoves(       int index, Bitboard enemy_and_empty);
};

#endif // CHESSBOARD_H
