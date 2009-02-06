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
    QObject::connect(board_widget, SIGNAL(pieceMoveInput(int,int)), &game, SLOT(move(int,int)));
    w.setCentralWidget(board_widget);
    /*
    AbstractChessGameModel ?
        SquareInfo squareInfo(int),
        Turn getTurn(),
        Bitboard getMoves(int)
    */
    w.show();
    return a.exec();
}
