#include "chessgame.h"

bool ChessGame::isPlayablePiece(int index)
{
	if (_board.getMoveNumber() % 2 == 0)
		return _board.isPieceWhite(index);
	else
		return _board.isPieceBlack(index);
}

void ChessGame::move(int src_index, int dst_index)
{
    // 1. validate
    //if (!(_board.getMoves(src_index) & 1 << dst_index))
    //    return;
	// 2. save current state to undo stack
	//history.append(_board);
	// 3. update board
    _board.move(src_index, dst_index);
	// 4. notify
	emit stateChanged();
}
