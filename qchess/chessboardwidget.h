#ifndef CHESSBOARDWIDGET_H
#define CHESSBOARDWIDGET_H

#include <QWidget>


class ChessGame;

struct Selection
{
	Selection() : squareIndex(-1), moveBits(0LL) {}
	int squareIndex;
	unsigned long long moveBits;
};


class ChessBoardWidget : public QWidget
{
    Q_OBJECT

public:
    ChessBoardWidget(ChessGame *game);

signals:
	void pieceMoveInput(int src_index, int dst_index);

protected:
	virtual void paintEvent(QPaintEvent *event);
	virtual void mouseMoveEvent(QMouseEvent *event);
	virtual void mousePressEvent(QMouseEvent *event);
	virtual void mouseReleaseEvent(QMouseEvent *event);

    ChessGame* _game;
    int _hot_square;
    Selection _selection;
};

#endif // CHESSBOARDWIDGET_H
