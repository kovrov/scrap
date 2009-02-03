#ifndef SELECTION_H
#define SELECTION_H

class Selection
{
public:
    Selection() : squareIndex(-1), moveBits(0LL) {}

    int squareIndex;
    unsigned long long moveBits;
};

#endif // SELECTION_H
