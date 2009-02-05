#ifndef SELECTION_H
#define SELECTION_H

struct Selection
{
    Selection() : squareIndex(-1), moveBits(0LL) {}
    int squareIndex;
    unsigned long long moveBits;
};

#endif // SELECTION_H
