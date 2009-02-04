#include <QApplication>
#include <QMainWindow>
#include <QObject>
#include "chessboardwidget.h"
#include "chessboard.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QMainWindow w;
    ChessBoard board;
    ChessBoardWidget* board_widget = new ChessBoardWidget(&board);
    QObject::connect(board_widget, SIGNAL(pieceMoveInput(int,int)), &board, SLOT(move(int,int)));
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
