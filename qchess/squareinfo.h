#ifndef SQUAREINFO_H
#define SQUAREINFO_H

enum COLOR { WHITE=1, BLACK };
enum PIECE { PAWN=1, KNIGHT, BISHOP, ROOK, QUEEN, KING };

class SquareInfo
{
public:
    SquareInfo(COLOR, PIECE);
    COLOR color;
    PIECE piece;
    const char* str;
};

#endif // SQUAREINFO_H
