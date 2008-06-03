#include "stdafx.h"
#include "view.h"
#include "../game/board.h"

#include <comdef.h>
#include <gdiplus.h>
using namespace Gdiplus;


int width = 40;
float corner = width - width / 3.0f;
const int gridBorder = 2;
const int gridPadding = width / 4;
const int gridWidth = width*10 + gridBorder*2 + gridPadding*2;
const Color  seaColor1(      0xEE, 0xF6, 0xFF);
const Color  seaColor2(0x7F, 0x99, 0xAE, 0xC6);
const Color shipColor1(      0x2F, 0x53, 0x7C);
const Color shipColor2(      0x53, 0x79, 0xA4);


void draw_ship(Graphics* graphics, int x, int y, int size, int disposition)
{
	graphics->SetSmoothingMode(SmoothingModeAntiAlias);
	Pen pen(shipColor1, corner);
	pen.SetLineJoin(LineJoinRound);
	graphics->DrawRectangle(&pen,
				x*width + corner/2, y*width + corner/2,
				width*(disposition==1?size:1) - corner, width*(disposition==0?size:1) - corner);
	SolidBrush brush(shipColor2);
	float k = 1.0f - 0.4f;
	for (int i=0; i < size; i++)
	{
		graphics->FillEllipse(&brush,
			i * (disposition==1?width:0) + x*width + width*k/2,
			i * (disposition==1?0:width) + y*width + width*k/2,
			width - width*k,
			width - width*k);
	}
	graphics->SetSmoothingMode(SmoothingModeDefault);
}


void draw_map_grid(Graphics* graphics)
{
	// border
	SolidBrush brush1(shipColor1);
	graphics->FillRectangle(&brush1, 0, 0, gridWidth, gridWidth);

	// background
	SolidBrush brush(seaColor1);
	graphics->FillRectangle(&brush, gridBorder, gridBorder,
				gridWidth-gridBorder*2, gridWidth-gridBorder*2);

	graphics->TranslateTransform(gridBorder+gridPadding, gridBorder+gridPadding);

	// ships
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

	// grid
	SolidBrush brush2(seaColor2);
	float k = 1.0f - 0.2f;
	for (int i=0; i < 11*11; i++)
	{
		int x = i % 11 * width;
		int y = i / 11 * width;
		graphics->FillRectangle(&brush2, x-3, y, 7, 1);
		graphics->FillRectangle(&brush2, x, y-3, 1, 7);
	}

	graphics->ResetTransform();
}


class BattleshipView
{
public:
	BattleshipView(HWND hwnd)
	  : m_mapBitmap (gridWidth, gridWidth)
	  , m_radarBitmap (gridWidth, gridWidth)
	{
		m_mapGraphics = Graphics::FromImage(&m_mapBitmap);
		m_radarGraphics = Graphics::FromImage(&m_radarBitmap);
		m_hwnd = hwnd;
	}
	~BattleshipView(void)
	{
		delete m_mapGraphics;
	}
	LONG OnPaint()
	{
		PAINTSTRUCT ps; 
		HDC hdc = BeginPaint(m_hwnd, &ps); 

		Graphics graphics(hdc);

		draw_map_grid(m_mapGraphics);
		//draw_radar_grid(hdc);

		graphics.DrawImage(&m_mapBitmap, 0, 0, m_mapBitmap.GetWidth(), m_mapBitmap.GetHeight());

		EndPaint(m_hwnd, &ps); 
		return 0;
	}
private:
	HWND m_hwnd;
	Graphics* m_mapGraphics;
	Bitmap m_mapBitmap;
	Graphics* m_radarGraphics;
	Bitmap m_radarBitmap;
	// drawing state
	void* m_radarShips;
	void* m_radarShots;
	bool m_radarShotActive;
	void* m_mapShips;
	void* m_mapShots;
	bool m_mapShotActive;
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
