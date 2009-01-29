#ifndef CHESSBOARDWIDGET_H
#define CHESSBOARDWIDGET_H

#include <QWidget>

class ChessBoard;

class ChessBoardWidget : public QWidget
{
    Q_OBJECT
public:
    ChessBoardWidget();
    ~ChessBoardWidget();
protected:
    void paintEvent(QPaintEvent *event);
    void mouseMoveEvent(QMouseEvent *event);

    ChessBoard* _board;
    int _hot_square;
};

#endif // CHESSBOARDWIDGET_H
