#include "stdafx.h"
#include "view.h"

#include "../game/board.h"

#include <comdef.h>
#include <gdiplus.h>
using namespace Gdiplus;

#include <boost/foreach.hpp>
#define foreach BOOST_FOREACH


int width = 40;
float corner = width - width / 3.0f;
const int gridBorder = 2;
const int gridPadding = width / 4;
const int gridWidth = width*10 + gridBorder*2 + gridPadding*2;
const Color  seaColor1(0xE8, 0xF0, 0xF8);
const Color  seaColor2(0xB0, 0xC0, 0xE0);
const Color shipColor1(0x30, 0x58, 0x80);
const Color shipColor2(0x58, 0x80, 0xA8);
const Color hitColor1( 0xE0, 0x90, 0x70);
const Color hitColor2( 0x90, 0x50, 0x40);

#define COLOR_ALPHA(color, alpha) Color((color).GetValue()&0x00FFFFFF|(DWORD)((alpha) << 24))


struct MapWidgetState
{
	MapWidgetState()
	  : bitmap (gridWidth, gridWidth)
	{
		graphics = Graphics::FromImage(&bitmap);
	}
	~MapWidgetState(void)
	{
		delete graphics;
	}

	Bitmap bitmap;
	Graphics* graphics;
};


void draw_ships(Graphics* graphics, const std::vector<board::Ship>& ships)
{
	graphics->SetSmoothingMode(SmoothingModeAntiAlias);

	foreach (board::Ship ship, ships)
	{
		board::ShipSegment front = ship.segments.front();
		board::ShipSegment back = ship.segments.back();

		Pen pen(shipColor1, corner);
		pen.SetLineJoin(LineJoinRound);
		graphics->DrawRectangle(&pen,
					front.pos.x*width + corner/2,
					front.pos.y*width + corner/2,
					(back.pos.x - front.pos.x + 1)*width - corner,
					(back.pos.y - front.pos.y + 1)*width - corner);

		SolidBrush brush(shipColor2);
		SolidBrush hitBrush1(hitColor1);
		Pen hitPen1(hitColor2, 2);
		HatchBrush hbrush(HatchStyleWideUpwardDiagonal,
			COLOR_ALPHA(seaColor1, 0x70),
			COLOR_ALPHA(seaColor1, 0x50));
		float k = 1.0f - 0.4f;
		float k2 = 1.0f - 0.5f;
		foreach (board::ShipSegment s, ship.segments)
		{
			if (s.active)
				graphics->FillEllipse(&brush,
							s.pos.x*width + width*k/2,
							s.pos.y*width + width*k/2,
							width - width*k,
							width - width*k);
			else
			{
				graphics->FillRectangle(&hbrush,
							s.pos.x*width,
							s.pos.y*width,
							width,
							width);
				graphics->FillEllipse(&hitBrush1,
							s.pos.x*width + width*k2/2,
							s.pos.y*width + width*k2/2,
							width - width*k2,
							width - width*k2);
				graphics->DrawEllipse(&hitPen1,
					s.pos.x*width + width*k2/2,
					s.pos.y*width + width*k2/2,
					width - width*k2,
					width - width*k2);
			}
		}
	}
	graphics->SetSmoothingMode(SmoothingModeDefault);
}


void draw_map_grid(Graphics* graphics, const std::vector<board::Ship>& ships)
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
	draw_ships(graphics, ships);

	// grid
	SolidBrush seaBrush2(COLOR_ALPHA(seaColor2, 0x80));
	float k = 1.0f - 0.2f;
	for (int i=0; i < 11*11; i++)
	{
		int x = i % 11 * width;
		int y = i / 11 * width;
		graphics->FillRectangle(&seaBrush2, x-3, y, 7, 1);
		graphics->FillRectangle(&seaBrush2, x, y-3, 1, 7);
	}

	graphics->ResetTransform();
}


void SetMapWidgetData(HWND hwnd, const std::vector<board::Ship>& ships)
{
	MapWidgetState* pState = reinterpret_cast<MapWidgetState*>(::GetWindowLongPtr(hwnd, GWLP_USERDATA));
	draw_map_grid(pState->graphics, ships);
}


LRESULT WINAPI MapWidgetWindowProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
	MapWidgetState* pState = reinterpret_cast<MapWidgetState*>(::GetWindowLongPtr(hwnd, GWLP_USERDATA));

	switch (msg)
	{
	case WM_NCCREATE:
		pState = new MapWidgetState();
		::SetWindowLongPtr(hwnd, GWLP_USERDATA, reinterpret_cast<LONG_PTR>(pState));
		return TRUE;

	case WM_NCDESTROY:
		::SetWindowLongPtr(hwnd, GWLP_USERDATA, NULL);
		delete pState;
		return 0;

	case WM_PAINT:
	{
	PAINTSTRUCT ps; 
	HDC hdc = ::BeginPaint(hwnd, &ps);
	Graphics graphics(hdc);
	graphics.DrawImage(&pState->bitmap, 0, 0, pState->bitmap.GetWidth(), pState->bitmap.GetHeight());
	::EndPaint(hwnd, &ps); 
	}
	return 0;

	default:
		break;
	}

	return DefWindowProc(hwnd, msg, wParam, lParam);
}


LPCTSTR InitMapWidget()
{
	// Initialize GDI+.
	ULONG_PTR gdiplusToken;
	GdiplusStartupInput gdiplusStartupInput;
	GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);
	// register class
	WNDCLASS wc;
	memset(&wc, 0, sizeof(wc));
	wc.lpszClassName = _T("MapWidget");
	wc.lpfnWndProc = &MapWidgetWindowProc;
	wc.hInstance = ::GetModuleHandle(NULL);
	wc.hCursor = ::LoadCursor(NULL, IDC_ARROW);
	//wc.cbWndExtra = sizeof(LONG_PTR);  // for passing state pointer
	//wc.hbrBackground = ::GetStockObject(WHITE_BRUSH);
	ATOM res = ::RegisterClass(&wc);
	assert (0 != res);
	return (LPCTSTR)MAKELONG(res, 0);
}


HWND CreateMapWidget(HWND hWndParent)
{
	static LPCTSTR registred_class = NULL;
	if (NULL == registred_class)
		registred_class = InitMapWidget();

	return ::CreateWindow(registred_class,
		_T(""),
		WS_CHILD|WS_VISIBLE,
		0,0,0,0,
		hWndParent,
		NULL,
		::GetModuleHandle(NULL),
		NULL);
}
