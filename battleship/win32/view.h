#pragma once

#include "../game/board.h"

HWND CreateMapWidget(HWND hWndParent);
void SetMapWidgetData(HWND hwnd, const std::vector<board::Ship>* ships);


// notifications

#define BSN_SQUARESELECTED WM_USER+1
struct BSNSquareInfo
{
	NMHDR hdr;
	board::Pos pos;
};
/* sample usage:

	case WM_NOTIFY:
		if (reinterpret_cast<NMHDR*>(lParam)->code == BSN_SQUARESELECTED)
		{
			BSNSquareInfo* si = reinterpret_cast<BSNSquareInfo*>(lParam);
		}
		break; 
*/


// messages

#define BSM_SETDATA WM_USER+1
