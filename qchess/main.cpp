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
	w.setCentralWidget(new ChessBoardWidget(&game));
    w.show();
    return a.exec();
}
