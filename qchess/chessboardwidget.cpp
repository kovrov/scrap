#include <QPainter>
#include <QMouseEvent>
#include "chessboardwidget.h"
#include "chessboard.h"

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
    setMouseTracking(true);
    _board = new ChessBoard;
    _hot_square = -1;
}

ChessBoardWidget::~ChessBoardWidget()
{
    delete _board;
}

void ChessBoardWidget::paintEvent(QPaintEvent *event)
{
    QColor white(0xFF, 0xCE, 0x9E);  // ffce9e
    QColor black(0xD1, 0x8B, 0x47);  // d18b47
    int side = qMin(width(), height());
    QPoint offset((width() - side + side % 8) / 2, (height() - side + side % 8) / 2);
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    painter.translate(offset);
    for (int i=0; i < 64; i++)
    {
        int x = i % 8;
        int y = 7 - i / 8;
        QRect rect(side / 8 * x, side / 8 * y, side / 8, side / 8);

        painter.setPen(Qt::NoPen);
        painter.setBrush(((x + y % 2) % 2) ? black : white);
        painter.drawRect(rect);
        if (i == _hot_square)
        {
            QColor white_tr(0xFF, 0xCE, 0x9E, 0x80);  // ffce9e
            QColor black_tr(0xD1, 0x8B, 0x47, 0x80);  // d18b47
            painter.setBrush(((x + y % 2) % 2) ? white_tr : black_tr);
            painter.drawRect(rect);
        }
        painter.setPen(Qt::black);
        painter.drawText(rect, _board->squareInfo(i));
    }
    // White Pawn
    QPainterPath path;
    path.moveTo(180.01563, 79.906825);
    path.cubicTo(170.90762, 79.906825, 163.51562, 87.298825, 163.51562, 96.406825);
    path.cubicTo(163.51562, 102.96328, 167.34695, 108.58985, 172.89063, 111.25058);
    path.cubicTo(172.46695, 149.02276, 155.04687, 124.25971, 155.04687, 144.56308);
    path.lineTo(155.01562, 150.53183);
    path.lineTo(204.98438, 150.53183);
    path.lineTo(204.95313, 144.56308);
    path.cubicTo(204.95313, 124.25975, 187.56438, 149.02243, 187.14063, 111.25058);
    path.cubicTo(192.67052, 108.58472, 196.51563, 102.95321, 196.51563, 96.406825);
    path.cubicTo(196.51563, 87.298825, 189.12363, 79.906825, 180.01563, 79.906825);
    path.closeSubpath();
    QPen p(QColor(0xDE,0xDE,0xDE));
    p.setWidth(5);
    painter.setPen(p);
    painter.setBrush(QBrush(QColor(0xBA,0xBA,0xBA)));
    painter.drawPath(path);
}

void ChessBoardWidget::mouseMoveEvent(QMouseEvent *event)
{
    int side = qMin(width(), height());
    int square = side / 8;
    QPoint offset((width() - side + side % 8) / 2, (height() - side + side % 8) / 2);
    QPoint pos = event->pos() - offset;
    int row =  pos.y() < 0 ? -1 : 7 - pos.y() / square;
    int file = pos.x() < 0 ? -1 :     pos.x() / square;
    int hot  = (row >= 0 && row < 8 && file >= 0 && file < 8)? row * 8 + file : -1;
    if (_hot_square != hot)
    {
        _hot_square = hot;
        update();
    }
}
