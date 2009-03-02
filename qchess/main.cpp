#include <QApplication>
#include <QMainWindow>
#include <QObject>
#include "chessboardwidget.h"
#include "chessgame.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QMainWindow w;
    ChessGame game;
    ChessBoardWidget* board_widget = new ChessBoardWidget(&game);
    w.setCentralWidget(board_widget);
    w.show();
    return a.exec();
}
