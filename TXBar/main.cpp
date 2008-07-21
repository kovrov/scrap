
#define WIN32_LEAN_AND_MEAN  // Exclude rarely-used stuff from Windows headers
// Windows Header Files:
#include <windows.h>
#include <windowsx.h>
#include <comdef.h>
#include <gdiplus.h>

// C/C++ RunTime Header Files
#include <stdlib.h>
#include <malloc.h>
#include <memory.h>
#include <tchar.h>
#include <assert.h>


#include "hooks.h"


#define ITEMS 6

#define SCALE 2.0f
#define PICSIZE 24
#define BORDERSIZE 12
#define CURSOR_SIZE 2

#define CURSOR_RADIUS ((PICSIZE+BORDERSIZE)*CURSOR_SIZE)
#define MAX_OFFSET ((PICSIZE * (SCALE-1)) * CURSOR_SIZE)

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam);

HHOOK g_llmouse_hhook = NULL;

void InitInstance(HINSTANCE hInstance, int nCmdShow)
{
	WNDCLASSEX wcex;
	memset(&wcex, 0, sizeof (WNDCLASSEX));
	wcex.cbSize         = sizeof (WNDCLASSEX);
	wcex.lpfnWndProc	= &WndProc;
	wcex.hInstance		= hInstance;
	wcex.hCursor		= ::LoadCursor(NULL, IDC_ARROW);
	//wcex.hbrBackground	= (HBRUSH)(COLOR_WINDOW + 1);
	wcex.lpszClassName	= _T("txbarwindow");
	::RegisterClassEx(&wcex);

	HWND hwnd_main = ::CreateWindowEx(WS_EX_LAYERED|WS_EX_TOPMOST|WS_EX_TOOLWINDOW,  // don't appear in the task bar 
	                             _T("txbarwindow"), _T("txbar"),
	                             WS_VISIBLE,
	                             CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,
								 NULL, NULL, hInstance, NULL);
	assert (hwnd_main);
}


int APIENTRY
_tWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPTSTR lpCmdLine, int nCmdShow)
{
	ULONG_PTR gdiplusToken;
	Gdiplus::GdiplusStartupInput m_gdiplusstartupinput;
	Gdiplus::GdiplusStartup(&gdiplusToken, &m_gdiplusstartupinput, NULL);

	InitInstance(hInstance, nCmdShow);

	MSG msg;
	while (::GetMessage(&msg, NULL, 0, 0))
	{
		::TranslateMessage(&msg);
		::DispatchMessage(&msg);
	}

	Gdiplus::GdiplusShutdown(gdiplusToken);

	return msg.wParam;
}



// TXBar stuff...

struct Padding
{
	Padding() {top = right = bottom = left = 0;}
	char top;
	char right;
	char bottom;
	char left;
};

struct Cell
{
	int center;
	float magnification;
	TCHAR* img_normal;
	TCHAR* img_big;
};

struct Row
{
	Cell cells[ITEMS];
	float offset;
	POINTS position;
	Padding padding;
};
Row row;

TCHAR* img_24[ITEMS] = {
		_T("intomain_24.png"),
		_T("intomini_24.png"),
		_T("todolist_24.png"),
		_T("mini_newevent_small.png"),
		_T("setting_24.png"),
		_T("exit_24.png")};
TCHAR* img_48[ITEMS] = {
		_T("intomain_48.png"),
		_T("intomini_48.png"),
		_T("todolist_48.png"),
		_T("newevent_big.png"),
		_T("setting_48.png"),
		_T("exit_48.png"),};


void DrawTXBar(HWND hwnd)
{
	RECT rcClient;
	::GetClientRect(hwnd, &rcClient);
	RECT rct;
	::GetWindowRect(hwnd, &rct);

	POINT ptWinPos = {rct.left, rct.top};
	SIZE sizeWindow = {rct.right-rct.left, rct.bottom-rct.top};

	HDC hdcScreen = ::GetDC(hwnd);
	HDC hdcMemory = ::CreateCompatibleDC(hdcScreen);
	HBITMAP hBitMap = ::CreateCompatibleBitmap(hdcScreen, sizeWindow.cx, sizeWindow.cy);
	::SelectObject(hdcMemory, hBitMap);
	
	Gdiplus::Graphics graphics(hdcMemory);
	//graphics.SetSmoothingMode(Gdiplus::SmoothingModeHighQuality);
	graphics.SetInterpolationMode(Gdiplus::InterpolationModeHighQualityBicubic);

	Gdiplus::Image title_img(_T("toolbarbktop.png"));
	graphics.DrawImage(&title_img,
		sizeWindow.cx/2 - title_img.GetWidth()/2, rcClient.top,
		title_img.GetWidth(), title_img.GetHeight());
	
	Gdiplus::Image toolbar_img(_T("toolbarbkbottom.png"));
	graphics.DrawImage(&toolbar_img,
		(int)(sizeWindow.cx/2 - title_img.GetWidth()/2), rcClient.top+title_img.GetHeight()-4,
		title_img.GetWidth(), toolbar_img.GetHeight());

// debug
//	Gdiplus::SolidBrush toolbar_brush(0x8090A0B0);
//	float dock_width = (float)(PICSIZE * ITEMS + BORDERSIZE * (ITEMS-1) + row.padding.left + row.padding.left);
//	float dock_height = (float)(row.padding.top + row.padding.bottom + PICSIZE);
//	float dock_x = sizeWindow.cx/2 - dock_width/2.0f;
//	graphics.FillRectangle(&toolbar_brush, dock_x, 0.0f, dock_width, dock_height);
//	Gdiplus::Pen toolbar_pen(0x80405060, 2);
//	graphics.DrawRectangle(&toolbar_pen, dock_x, 0.0f, dock_width, dock_height);

	Gdiplus::REAL y = (float)(row.padding.top + title_img.GetHeight());
	Gdiplus::REAL half_shift = row.offset / 2.0f;
	for (int i=0; i < ITEMS; i++)
	{
		Cell& cell = row.cells[i];
		Gdiplus::REAL icon_size = PICSIZE * cell.magnification;
		Gdiplus::REAL diff = icon_size - PICSIZE;
		Gdiplus::REAL center = cell.center + diff / 2.0f - half_shift;

		Gdiplus::Image img((icon_size > 24) ? cell.img_big : cell.img_normal);
		graphics.DrawImage(&img,
					row.position.x + center - icon_size / 2.0f, y,
					icon_size, icon_size);

// debug
//		Gdiplus::SolidBrush debug_icon_brush(0x80000080);
//		graphics.FillRectangle(&debug_icon_brush,
//					row.position.x + center - icon_size / 2.0f, y,
//					icon_size, icon_size);
//		Gdiplus::Pen debug_icon_pen(0xFF000080, 2);
//		graphics.DrawRectangle(&debug_icon_pen,
//					row.position.x + center - icon_size / 2.0f, y,
//					icon_size, icon_size);

		half_shift -= diff;
	}

// debug
//	Gdiplus::Pen debug_cell_pen(0xFFFF0000);
//	for (int i=0; i < ITEMS; i++)
//	{
//		Cell& cell = row.cells[i];
//		Gdiplus::REAL x = row.position.x + cell.center - (PICSIZE+BORDERSIZE) / 2.0f;
//		graphics.DrawRectangle(&debug_cell_pen,
//					x, 0.0f,
//					(float)(PICSIZE+BORDERSIZE), (float)(PICSIZE+BORDERSIZE/2));
//	}

	POINT ptSrc = {0, 0};
	BLENDFUNCTION blend_fn = {AC_SRC_OVER,  // the only blend operation defined
	                          0,  // reserved?
	                          0xFF,  // use per-pixel alpha values
	                          AC_SRC_ALPHA};  // AlphaFormat
	BOOL bRet = ::UpdateLayeredWindow(hwnd, hdcScreen, &ptWinPos, &sizeWindow,
	                                  hdcMemory, &ptSrc, 0, &blend_fn, 2);
	graphics.ReleaseHDC(hdcMemory);
	::ReleaseDC(hwnd, hdcScreen);
	::DeleteObject(hBitMap);
	::DeleteDC(hdcMemory);
}


LRESULT OnCreate(HWND hwnd)
{
	row.padding.top = 6;
	row.padding.bottom = row.padding.left = row.padding.right = BORDERSIZE/2;
	row.position.x = (SHORT)(MAX_OFFSET/2);
	row.offset = 0.0f;

	RECT r;
	::GetWindowRect(hwnd, &r);
	int screen_width = ::GetSystemMetrics(SM_CXSCREEN);
	::MoveWindow(hwnd,
	             screen_width/2 - (int)((PICSIZE+BORDERSIZE) * ITEMS + MAX_OFFSET)/2,
				 0,
	             (int)((PICSIZE+BORDERSIZE) * ITEMS + MAX_OFFSET),
				 (int)(row.padding.top + PICSIZE * SCALE + 40),
	             FALSE);

	for (int i=0; i < ITEMS; i++)
	{
		Cell& cell = row.cells[i];
		cell.center = (PICSIZE+BORDERSIZE) * i + (PICSIZE+BORDERSIZE) / 2;
		cell.magnification = 1.0f;
		cell.img_normal = img_24[i];
		cell.img_big = img_48[i];
	}

	DrawTXBar(hwnd);
	return 0;
}


void OnMouseMove(HWND hwnd, UINT nFlags, POINTS point)
{
	if (point.x < row.position.x || point.x > row.position.x + (PICSIZE+BORDERSIZE)*ITEMS)
	{
		row.offset = 0.0f;
		for (int i=0; i < ITEMS; i++)
		{
			Cell& cell = row.cells[i];
			cell.magnification = 1.0f;
		}
		DrawTXBar(hwnd);
		return;
	}

	row.offset = -MAX_OFFSET;
	bool offset_needed = true;
	for (int i=0; i < ITEMS; i++)
	{
		Cell& cell = row.cells[i];
		float distance = (float)abs(row.position.x + cell.center - point.x);

		// magnification is scaled from 1.0f (no magnification) to SCALE (full magnification)
		if (distance > CURSOR_RADIUS)
			cell.magnification = 1.0f;
		else
		{
			cell.magnification = 1.0f + (SCALE - 1.0f) * (1.0f - distance / CURSOR_RADIUS);
			if (point.x < row.position.x + CURSOR_RADIUS)
			{
				float real_size = PICSIZE * cell.magnification;
				row.offset += (real_size - PICSIZE) * 2;
				offset_needed = false;
			}
		}
	}

	if (offset_needed)
		row.offset = MAX_OFFSET;

	DrawTXBar(hwnd);
}


void OnTimer(HWND hwnd)
{
}


LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	switch (message)
	{
	case WM_CREATE:
		return OnCreate(hWnd);

	case WM_MOUSEMOVE:
		// the hook needed to get mouse movement on transparent areas
		if (NULL == g_llmouse_hhook)
			g_llmouse_hhook = setLLMouseHook(hWnd);
		break;

	case WM_MOUSEMOVE_GLOBAL:
		if (wParam == MM_IN)
		{
			OnMouseMove(hWnd, 0, MAKEPOINTS(lParam));
		}
		else // MM_OUT
		{
			clearLLMouseHook(g_llmouse_hhook);
			g_llmouse_hhook = NULL;
		}
		return 0;

	case WM_TIMER:
		OnTimer(hWnd);
		break;

	case WM_DESTROY:
		::PostQuitMessage(0);
		break;

	case WM_NCCALCSIZE:  // http://msdn.microsoft.com/library/ms632634.aspx
		return 0;  // make client area the same size as window

	default:
		return ::DefWindowProc(hWnd, message, wParam, lParam);
	}
	return 0;
}
