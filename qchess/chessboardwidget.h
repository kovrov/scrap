#ifndef CHESSBOARDWIDGET_H
#define CHESSBOARDWIDGET_H

#include <QWidget>
#include "selection.h"

class ChessBoard;


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
    Selection _selection;
};

#endif // CHESSBOARDWIDGET_H
