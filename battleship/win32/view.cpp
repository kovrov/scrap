#include "stdafx.h"
#include "view.h"

#include <comdef.h>
#include <gdiplus.h>
using namespace Gdiplus;


void draw_radar_grid(HDC hdc)
{
	Graphics graphics(hdc);
	graphics.SetSmoothingMode(SmoothingModeAntiAlias);
	int width = 20;
	int corner = 16;

	int x = 30;
	int y = 30;
	Pen pen(Color(255, 0, 0, 0), corner);
	pen.SetLineJoin(LineJoinRound);
	graphics.DrawRectangle(&pen, x + corner/2, y + corner/2, width - corner, width*2 - corner);

	x = 60;
	y = 30;
	Pen pen2(Color(255, 0, 0, 0), corner);
	pen2.SetAlignment(PenAlignmentInset);
	graphics.DrawRectangle(&pen2, x, y, width, width*2);
}


class BattleshipView
{
public:
	BattleshipView(HWND hwnd) { m_hwnd = hwnd; }
	~BattleshipView(void) {}
	LONG OnPaint()
	{
		PAINTSTRUCT ps; 
		HDC hdc = BeginPaint(m_hwnd, &ps); 

		RECT rc; 
		GetClientRect(m_hwnd, &rc);
		FillRect(hdc, &rc, (HBRUSH)(COLOR_WINDOW+1));

		draw_radar_grid(hdc);
		//draw_map_grid(hdc);

		EndPaint(m_hwnd, &ps); 
		return 0;
	}
private:
	HWND m_hwnd;
};





BOOL InitView()
{
	// Initialize GDI+.
	ULONG_PTR gdiplusToken;
	GdiplusStartupInput gdiplusStartupInput;
	GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);
	// register class
	WNDCLASSEX	wcx;
	memset(&wcx, 0, sizeof(wcx));
	wcx.cbSize        = sizeof(wcx);
	wcx.lpfnWndProc   = &ViewWndProc;
	wcx.cbWndExtra    = sizeof(void*);
	wcx.hInstance     = GetModuleHandle(NULL);
	wcx.hCursor       = LoadCursor(NULL, IDC_ARROW);
	wcx.lpszClassName = VIEW_CLASS;	
	return RegisterClassEx(&wcx) ? TRUE : FALSE;
}


LRESULT WINAPI ViewWndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
	BattleshipView* ptv = (BattleshipView*)GetWindowLong(hwnd, 0);

	switch (msg)
	{
	case WM_NCCREATE:
		ptv = new BattleshipView(hwnd);
		SetWindowLong(hwnd, 0, (LONG)ptv);
		return TRUE;

	case WM_NCDESTROY:
		delete ptv;
		return 0;

	case WM_PAINT:
		return ptv->OnPaint();

	default:
		break;
	}

	return DefWindowProc(hwnd, msg, wParam, lParam);
}
