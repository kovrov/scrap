#include "stdafx.h"
#include "view.h"

#include <comdef.h>
#include <gdiplus.h>
using namespace Gdiplus;


int width = 50;
int corner = width - width / 3;
unsigned char seaColor1[]  = {0xEE, 0xF6, 0xFF};
unsigned char seaColor2[]  = {0xda, 0xe6, 0xf4};
unsigned char shipColor1[] = {0x2F, 0x53, 0x7C};
unsigned char shipColor2[] = {0x53, 0x79, 0xA4};


void draw_ship(Graphics& graphics, int x, int y, int size, int disposition)
{
	Pen pen(Color(shipColor1[0], shipColor1[1], shipColor1[2]), corner);
	pen.SetLineJoin(LineJoinRound);
	graphics.DrawRectangle(&pen,
				x*width + corner/2, y*width + corner/2,
				width*(disposition==1?size:1) - corner, width*(disposition==0?size:1) - corner);
	SolidBrush brush(Color(shipColor2[0], shipColor2[1], shipColor2[2]));
	float k = 1.0 - 0.4;
	for (int i=0; i < size; i++)
	{
		graphics.FillEllipse(&brush,
			i * (disposition==1?width:0) + x*width + width*k/2,
			i * (disposition==1?0:width) + y*width + width*k/2,
			width - width*k,
			width - width*k);
	}
}


void draw_radar_grid(HDC hdc)
{
	Graphics graphics(hdc);
	graphics.SetSmoothingMode(SmoothingModeAntiAlias);

	SolidBrush brush(Color(seaColor1[0], seaColor1[1], seaColor1[2]));
	graphics.FillRectangle(&brush, 0, 0, width*10, width*10);

	SolidBrush brush2(Color(seaColor2[0], seaColor2[1], seaColor2[2]));
	float k = 1.0 - 0.2;
	for (int i=0; i<100; i++)
	{
		int x = i % 10 * width;
		int y = i / 10 * width;
		graphics.FillEllipse(&brush2,
			x + width*k/2,
			y + width*k/2,
			width - width*k,
			width - width*k);
	}

	int x = 2;
	int y = 1;
	int size = 2;
	int disposition = 0; // vertical
	draw_ship(graphics, x, y, size, disposition);

	x = 4;
	y = 2;
	size = 3;
	disposition = 1; // horizontal
	draw_ship(graphics, x, y, size, disposition);
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

		//RECT rc; 
		//GetClientRect(m_hwnd, &rc);
		//FillRect(hdc, &rc, (HBRUSH)(COLOR_WINDOW+1));

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
