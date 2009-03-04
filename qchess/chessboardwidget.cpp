#include <QPainter>
#include <QMouseEvent>
#include "chessboardwidget.h"
#include "chessgame.h"
#include "data/draw.h"


int GetSquareIndex(const QRect &rect, const QPoint &ev_pos)
{
	int board_side = qMin(rect.width(), rect.height());
	QPoint offset((rect.width() - board_side + board_side % 8) / 2, (rect.height() - board_side + board_side % 8) / 2);
	QPoint pos = ev_pos - offset;
	int row =  pos.y() < 0 ? -1 : 7 - pos.y() / (board_side / 8);
	int file = pos.x() < 0 ? -1 :     pos.x() / (board_side / 8);
	return (row >= 0 && row < 8 && file >= 0 && file < 8)? row * 8 + file : -1;
}



ChessBoardWidget::ChessBoardWidget(ChessGame *game)
{
    _game = game;
    _hot_square = -1;
    setMouseTracking(true);
    initDraw();
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

        PIECE piece = _game->getPiece(i);
        if (piece == NONE)
            continue;

        painter.save();
        painter.translate(square_rect.topLeft());
        qreal scale = board_side / 8;
        painter.scale(scale, scale);
        DrawData *dd = &cachedDrawData[piece];
        painter.setBrush(dd->brush);
        painter.setPen(dd->pen);
        painter.drawPath(dd->path);
        painter.setBrush(dd->brush2);
        painter.setPen(dd->pen2);
        painter.drawPath(dd->path2);
        painter.restore();
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
    if (!_game->isPlayablePiece(index))
		return;
    _selection.squareIndex = index;
    _selection.moveBits = _game->getPossibleMoves(index);
	update();
}

void ChessBoardWidget::mouseReleaseEvent(QMouseEvent *event)
{
	if (event->button() != Qt::LeftButton)
		return;

	int index = GetSquareIndex(rect(), event->pos());
	if (_selection.moveBits & 1LL << index)
		_game->move(_selection.squareIndex, index);

	_selection.squareIndex = -1;
	_selection.moveBits = 0LL;
	update();
}

void ChessBoardWidget::leaveEvent(QEvent *event)
{
    if (_hot_square != -1)
    {
        _hot_square = -1;
        update();
    }
}
