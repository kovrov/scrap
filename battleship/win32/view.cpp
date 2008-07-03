#include "stdafx.h"
#include "view.h"

#include "../game/board.h"

#include <comdef.h>
#include <gdiplus.h>

#include <assert.h>

#include <boost/foreach.hpp>
#define foreach BOOST_FOREACH


int width = 40;
float corner = width - width / 3.0f;
const int gridPadding = width / 4;
const int gridWidth = width*10 + gridPadding*2;

#define COLOR_ALPHA(color, alpha) ((color) & 0x00FFFFFF|(DWORD)((alpha) << 24))


struct MapWidgetState
{
	MapWidgetState()
	  : bitmap (gridWidth, gridWidth)
	{
		graphics = Gdiplus::Graphics::FromImage(&bitmap);
		theme[SEA_BACKGROUND_COLOR]  = 0xFFE8F0F8;
		theme[SEA_FOREROUND_COLOR]   = 0xFFB0C0E0;
		theme[SHIP_FOREGROUND_COLOR] = 0xFF305880;
		theme[SHIP_BACKGROUND_COLOR] = 0xFF5880A8;
		theme[HIT_FOREGROUND_COLOR]  = 0xFF905040;
		theme[HIT_BACKGROUND_COLOR]  = 0xFFE09070;
	}
	~MapWidgetState(void)
	{
		delete graphics;
	}

	Gdiplus::Bitmap bitmap;
	Gdiplus::Graphics* graphics;
	// default color values
	DWORD theme[COLORS_LENGHT];
};


void draw_shots(Gdiplus::Graphics* graphics, const std::vector<board::Shot>* shots, Gdiplus::ARGB* theme)
{
	assert (shots != NULL);
	graphics->SetSmoothingMode(Gdiplus::SmoothingModeAntiAlias);

	Gdiplus::SolidBrush hitForegroundBrush(COLOR_ALPHA(theme[HIT_FOREGROUND_COLOR], 0x60));
	Gdiplus::SolidBrush hitBackgroundBrush(theme[HIT_BACKGROUND_COLOR]);
	Gdiplus::Pen hitForegroundPen(theme[HIT_FOREGROUND_COLOR], 4);
	float k = 1.0f - 0.3f;
	float k2 = 1.0f - 0.5f;
	foreach (board::Shot shot, *shots)
	{
		if (board::MISS == shot.result)
		{
			graphics->FillEllipse(&hitForegroundBrush,
						shot.x*width + width*k/2,
						shot.y*width + width*k/2,
						width - width*k,
						width - width*k);
		}
		else
		{
			graphics->FillEllipse(&hitBackgroundBrush,
						shot.x*width + width*k2/2,
						shot.y*width + width*k2/2,
						width - width*k2,
						width - width*k2);
			graphics->DrawEllipse(&hitForegroundPen,
						shot.x*width + width*k2/2,
						shot.y*width + width*k2/2,
						width - width*k2,
						width - width*k2);
		}
	}
	graphics->SetSmoothingMode(Gdiplus::SmoothingModeDefault);
}


void draw_ships(Gdiplus::Graphics* graphics, const std::vector<board::Ship>* ships, Gdiplus::ARGB* theme)
{
	assert (ships != NULL);
	graphics->SetSmoothingMode(Gdiplus::SmoothingModeAntiAlias);

	foreach (board::Ship ship, *ships)
	{
		board::ShipSegment front = ship.segments.front();
		board::ShipSegment back = ship.segments.back();

		Gdiplus::Pen pen(theme[SHIP_FOREGROUND_COLOR], corner);
		pen.SetLineJoin(Gdiplus::LineJoinRound);
		graphics->DrawRectangle(&pen,
					front.pos.x*width + corner/2,
					front.pos.y*width + corner/2,
					(back.pos.x - front.pos.x + 1)*width - corner,
					(back.pos.y - front.pos.y + 1)*width - corner);

		Gdiplus::SolidBrush brush(theme[SHIP_BACKGROUND_COLOR]);
		Gdiplus::HatchBrush hbrush(Gdiplus::HatchStyleWideUpwardDiagonal,
			COLOR_ALPHA(theme[SEA_BACKGROUND_COLOR], 0xC0),
			COLOR_ALPHA(theme[SEA_BACKGROUND_COLOR], 0xA0));
		float k = 1.0f - 0.4f;
		bool ship_active = false;
		foreach (board::ShipSegment s, ship.segments)
		{
			if (s.active)
			{
				graphics->FillEllipse(&brush,
							s.pos.x*width + width*k/2,
							s.pos.y*width + width*k/2,
							width - width*k,
							width - width*k);
				ship_active = true;
			}
			else
			{
				graphics->SetSmoothingMode(Gdiplus::SmoothingModeDefault);
				graphics->FillRectangle(&hbrush,
							s.pos.x*width,
							s.pos.y*width,
							width,
							width);
				graphics->SetSmoothingMode(Gdiplus::SmoothingModeAntiAlias);
			}
		}
	}
	graphics->SetSmoothingMode(Gdiplus::SmoothingModeDefault);
}


void draw_map_grid(Gdiplus::Graphics* graphics, const std::vector<board::Ship>* ships, const std::vector<board::Shot>* shots, Gdiplus::ARGB* theme)
{
	// border
	Gdiplus::SolidBrush brush1(theme[SHIP_FOREGROUND_COLOR]);
	graphics->FillRectangle(&brush1, 0, 0, gridWidth, gridWidth);

	// background
	Gdiplus::SolidBrush brush(theme[SEA_BACKGROUND_COLOR]);
	graphics->FillRectangle(&brush, 0, 0,
				gridWidth, gridWidth);

	graphics->TranslateTransform((Gdiplus::REAL)(gridPadding), (Gdiplus::REAL)(gridPadding));

	// grid
	Gdiplus::SolidBrush seaBrush2(COLOR_ALPHA(theme[SEA_FOREROUND_COLOR], 0x80));
	float k = 1.0f - 0.2f;
	for (int i=0; i < 11*11; i++)
	{
		int x = i % 11 * width;
		int y = i / 11 * width;
		graphics->FillRectangle(&seaBrush2, x-3, y, 7, 1);
		graphics->FillRectangle(&seaBrush2, x, y-3, 1, 7);
	}

	// ships and shots
	if (ships != NULL)
		draw_ships(graphics, ships, theme);
	if (shots != NULL)
		draw_shots(graphics, shots, theme);
	if (shots != NULL && shots->size() > 0)
	{
		const board::Shot& pos = shots->back();
		Gdiplus::SolidBrush brush_red(COLOR_ALPHA(theme[HIT_BACKGROUND_COLOR], 0x20));
		graphics->SetSmoothingMode(Gdiplus::SmoothingModeAntiAlias);
		graphics->FillEllipse(&brush_red,
			pos.x * width - width/5,
			pos.y * width - width/5,
			width + width/5*2,
			width + width/5*2);
		graphics->SetSmoothingMode(Gdiplus::SmoothingModeDefault);
	}

	graphics->ResetTransform();
}


void SetMapWidgetData(HWND hwnd, const std::vector<board::Ship>* ships, const std::vector<board::Shot>* shots)
{
	MapWidgetState* pState = reinterpret_cast<MapWidgetState*>(::GetWindowLongPtr(hwnd, GWLP_USERDATA));
	if (NULL == pState)  // assert
		return;
	draw_map_grid(pState->graphics, ships, shots, pState->theme);
	::InvalidateRgn(hwnd, NULL, FALSE);  // force redraw
}


void SetMapWidgetThemeColor(HWND hwnd, int color, DWORD value)
{
	MapWidgetState* pState = reinterpret_cast<MapWidgetState*>(::GetWindowLongPtr(hwnd, GWLP_USERDATA));
	if (NULL == pState)  // assert
		return;
	pState->theme[color] = value;
	SetMapWidgetData(hwnd, NULL, NULL);
}


LRESULT WINAPI MapWidgetWindowProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
	MapWidgetState* pState = reinterpret_cast<MapWidgetState*>(::GetWindowLongPtr(hwnd, GWLP_USERDATA));

	switch (msg)
	{
	case WM_NCCREATE:
		pState = new MapWidgetState();
		::SetWindowLongPtr(hwnd, GWLP_USERDATA, reinterpret_cast<LONG_PTR>(pState));
		SetMapWidgetData(hwnd, NULL, NULL);
		return TRUE;

	case WM_NCDESTROY:
		::SetWindowLongPtr(hwnd, GWLP_USERDATA, NULL);
		delete pState;
		return 0;

	case WM_PAINT:
		{
		PAINTSTRUCT ps; 
		HDC hdc = ::BeginPaint(hwnd, &ps);

		Gdiplus::Graphics graphics(hdc);
		graphics.DrawImage(&pState->bitmap, 0, 0, pState->bitmap.GetWidth(), pState->bitmap.GetHeight());

		::EndPaint(hwnd, &ps); 
		}
		return 0;

	case WM_GETMINMAXINFO: {
		MINMAXINFO* minmaxinfo = reinterpret_cast<MINMAXINFO*>(lParam);
		minmaxinfo->ptMinTrackSize.x = minmaxinfo->ptMinTrackSize.y = gridWidth;
		minmaxinfo->ptMaxTrackSize.y = minmaxinfo->ptMaxTrackSize.x = gridWidth;
		} break;

	case WM_NCCALCSIZE:  // at which point this info is asked?
		if (wParam)
		{
			NCCALCSIZE_PARAMS* size_param = reinterpret_cast<NCCALCSIZE_PARAMS*>(lParam);
			size_param->rgrc[0].right = size_param->rgrc[0].left + gridWidth;
			size_param->rgrc[0].bottom = size_param->rgrc[0].top + gridWidth;
			size_param->lppos->cx = gridWidth;
			size_param->lppos->cy = gridWidth;
		}
		else
		{
			RECT* rect = reinterpret_cast<RECT*>(lParam);
			rect->bottom = rect->top + gridWidth;
			rect->right = rect->left + gridWidth;
		}
		return 0;

	case WM_WINDOWPOSCHANGING: {  // in case parent ask for an invalid window size...
		WINDOWPOS* pos = reinterpret_cast<WINDOWPOS*>(lParam);
		pos->cx = gridWidth;
		pos->cy = gridWidth;
		} break;

	case WM_LBUTTONUP:
		{
		int x = LOWORD(lParam) - gridPadding;
		int y = HIWORD(lParam) - gridPadding;
		if (x < 0 || y < 0)
			return 0;
		if (x / width > 9 || y / width > 9)
			return 0;
		BSNSquareInfo si = { { hwnd, ::GetWindowLong(hwnd, GWL_ID), BSN_SQUARESELECTED },
							board::Pos(x / width, y / width) };
		::SendMessage(::GetParent(hwnd), WM_NOTIFY, (WPARAM)hwnd, (LPARAM)&si.hdr);
		}
		break;
	}

	return DefWindowProc(hwnd, msg, wParam, lParam);
}


LPCTSTR InitMapWidget()
{
	// Initialize GDI+.
	ULONG_PTR token;
	Gdiplus::GdiplusStartupInput input;
	//input.SuppressBackgroundThread = TRUE;
	Gdiplus::GdiplusStartup(&token, &input, NULL);
	// register class
	WNDCLASS wc;
	memset(&wc, 0, sizeof(wc));
	wc.lpszClassName = _T("MapWidget");
	wc.lpfnWndProc = &MapWidgetWindowProc;
	wc.hInstance = ::GetModuleHandle(NULL);
	wc.hCursor = ::LoadCursor(NULL, IDC_ARROW);
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

	HWND hwnd = ::CreateWindow(registred_class,
				_T(""),
				WS_CHILD|WS_VISIBLE,
				0,0,0,0,
				hWndParent,
				NULL,
				::GetModuleHandle(NULL),
				NULL);
	return hwnd;
}
