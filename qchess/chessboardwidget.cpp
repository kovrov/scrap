#include <QPainter>
#include "chessboardwidget.h"

const char* coords[] = {
    "a1","b1","c1","d1","e1","f1","g1","h1",
    "a2","b2","c2","d2","e2","f2","g2","h2",
    "a3","b3","c3","d3","e3","f3","g3","h3",
    "a4","b4","c4","d4","e4","f4","g4","h4",
    "a5","b5","c5","d5","e5","f5","g5","h5",
    "a6","b6","c6","d6","e6","f6","g6","h6",
    "a7","b7","c7","d7","e7","f7","g7","h7",
    "a8","b8","c8","d8","e8","f8","g8","h8"};

ChessBoardWidget::ChessBoardWidget()
{
}


void ChessBoardWidget::paintEvent(QPaintEvent *event)
{
    int side = qMin(width(), height());
    QColor white(0xFF, 0xCE, 0x9E);  // ffce9e
    QColor black(0xD1, 0x8B, 0x47);  // d18b47
    QPainter painter(this);

    for (int i=0; i < 64; i++)
    {
        int x = i % 8;
        int y = 7 - i / 8;
        QRect rect(side/8*x, side/8*y, side/8, side/8);

        painter.setPen(Qt::NoPen);
        painter.setBrush(((x + y % 2) % 2) ? white : black);
        painter.drawRect(rect);
    }
}
