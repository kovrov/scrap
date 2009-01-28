#ifndef CHESSBOARDWIDGET_H
#define CHESSBOARDWIDGET_H

#include <QWidget>

class ChessBoardWidget : public QWidget
{
    Q_OBJECT
public:
    ChessBoardWidget();
protected:
    void paintEvent(QPaintEvent *event);
};

#endif // CHESSBOARDWIDGET_H
