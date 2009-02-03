#include <QPainter>
#include <QMouseEvent>
#include "chessboardwidget.h"
#include "chessboard.h"
#include "squareinfo.h"
#include "data/draw.h"

const char* coords[] = {
    "a1","b1","c1","d1","e1","f1","g1","h1",
    "a2","b2","c2","d2","e2","f2","g2","h2",
    "a3","b3","c3","d3","e3","f3","g3","h3",
    "a4","b4","c4","d4","e4","f4","g4","h4",
    "a5","b5","c5","d5","e5","f5","g5","h5",
    "a6","b6","c6","d6","e6","f6","g6","h6",
    "a7","b7","c7","d7","e7","f7","g7","h7",
    "a8","b8","c8","d8","e8","f8","g8","h8"};

int GetSquareIndex(const QRect &rect, const QPoint &ev_pos)
{
	int board_side = qMin(rect.width(), rect.height());
	QPoint offset((rect.width() - board_side + board_side % 8) / 2, (rect.height() - board_side + board_side % 8) / 2);
	QPoint pos = ev_pos - offset;
	int row =  pos.y() < 0 ? -1 : 7 - pos.y() / (board_side / 8);
	int file = pos.x() < 0 ? -1 :     pos.x() / (board_side / 8);
	return (row >= 0 && row < 8 && file >= 0 && file < 8)? row * 8 + file : -1;
}

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
	int board_side = qMin(width(), height());
	QPoint offset((width() - board_side + board_side % 8) / 2, (height() - board_side + board_side % 8) / 2);
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    painter.translate(offset);
    for (int i=0; i < 64; i++)
    {
        int x = i % 8;
        int y = 7 - i / 8;
		QRect square_rect(board_side / 8 * x, board_side / 8 * y, board_side / 8, board_side / 8);

        painter.setPen(Qt::NoPen);
        painter.setBrush(((x + y % 2) % 2) ? black : white);
        if (i == _hot_square)
        {
            QColor white_tr(0xFF, 0xCE, 0x9E, 0x40);  // ffce9e
            QColor black_tr(0xD1, 0x8B, 0x47, 0x40);  // d18b47
            painter.setBrush(((x + y % 2) % 2) ? white_tr : black_tr);
        }

        if (_selection.squareIndex != -1)
        {
            if (_selection.moveBits & 1LL << i)
            {
                QColor white_tr(0xFF, 0xCE, 0x9E, 0x80);  // ffce9e
                QColor black_tr(0xD1, 0x8B, 0x47, 0x80);  // d18b47
                painter.setBrush(((x + y % 2) % 2) ? white_tr : black_tr);
            }
        }

        painter.drawRect(square_rect);

        SquareInfo si = _board->squareInfo(i);
        if (si.color != 0)
        {
            painter.save();
            painter.translate(square_rect.center());
			qreal scale = board_side / 8;
            painter.scale(scale, scale);

			QPen p(QColor(0x00,0x00,0x00));
            p.setWidth(5);
            painter.setPen(p);
			painter.setBrush(QBrush((si.color == WHITE) ? QColor(0xFF,0xFF,0xFF) : QColor(0x00,0x00,0x00)));
            switch (si.piece)
            {
            case PAWN:
                draw_pawn(&painter);
                break;
            case KNIGHT:
                draw_knight(&painter);
                break;
            case BISHOP:
                draw_bishop(&painter);
                break;
            case ROOK:
                draw_rook(&painter);
                break;
            case QUEEN:
                draw_queen(&painter);
                break;
            case KING:
                draw_king(&painter);
                break;
            }

            painter.restore();
        }
    }
}

void ChessBoardWidget::mouseMoveEvent(QMouseEvent *event)
{
	int hot = GetSquareIndex(rect(), event->pos());
    if (_hot_square != hot)
    {
        _hot_square = hot;
        update();
    }
}

void ChessBoardWidget::mousePressEvent(QMouseEvent *event)
{
	if (event->button() != Qt::LeftButton)
		return;
	int index = GetSquareIndex(rect(), event->pos());
	if (index < 0 || index > 63)
		return;
	SquareInfo si = _board->squareInfo(index);
    _selection.squareIndex = index;
    _selection.moveBits = _board->getMoves(index);
}
