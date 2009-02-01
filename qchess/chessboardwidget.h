#ifndef CHESSBOARDWIDGET_H
#define CHESSBOARDWIDGET_H

#include <QWidget>

class ChessBoard;

struct DragPiece
{
	DragPiece() : index (-1) {}
	int index;
	QPainterPath fillPath;
	QPen fillPen;
	QBrush fillBrush;
};

class ChessBoardWidget : public QWidget
{
    Q_OBJECT
public:
    ChessBoardWidget();
	virtual ~ChessBoardWidget();
protected:
	virtual void paintEvent(QPaintEvent *event);
	virtual void mouseMoveEvent(QMouseEvent *event);
	virtual void mousePressEvent(QMouseEvent *event);

    ChessBoard* _board;
    int _hot_square;
	DragPiece _dragPiece;
};

#endif // CHESSBOARDWIDGET_H
