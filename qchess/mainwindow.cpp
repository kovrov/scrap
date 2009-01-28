#include "mainwindow.h"
#include "chessboardwidget.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setCentralWidget(new ChessBoardWidget());
}

MainWindow::~MainWindow()
{
}
