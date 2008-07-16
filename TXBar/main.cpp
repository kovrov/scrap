#include "stdafx.h"

#define ITEMS 6

#define SCALE 2.0f
#define PICSIZE 24
#define BORDERSIZE 12
#define CURSOR_SIZE 2

#define CURSOR_RADIUS ((PICSIZE+BORDERSIZE)*CURSOR_SIZE)
#define MAX_OFFSET ((PICSIZE+BORDERSIZE) * (SCALE-1) * CURSOR_SIZE)

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam);

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

	HWND hWnd = ::CreateWindowEx(WS_EX_LAYERED|WS_EX_TOPMOST|WS_EX_TOOLWINDOW,  // don't appear in the task bar 
	                             _T("txbarwindow"), _T("txbar"),
	                             WS_VISIBLE,
	                             CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,
								 NULL, NULL, hInstance, NULL);
	assert (hWnd);
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

struct Cell
{
	int center;
	float magnification;
};

struct Row
{
	int left;
	Cell cells[ITEMS];
	float offset;
};
Row row;

Gdiplus::Rect rcTool[6];
Gdiplus::Rect rcBack[6];
RECT rcRange[6];
BLENDFUNCTION g_Blend = {AC_SRC_OVER,  // the only blend operation defined
                         0,  // reserved?
                         0xFF,  // use per-pixel alpha values
                         AC_SRC_ALPHA};  // AlphaFormat


void DrawTXBar(HWND hwnd)
{
	RECT rcClient;
	::GetClientRect(hwnd, &rcClient);
	RECT rct;
	::GetWindowRect(hwnd, &rct);

	POINT ptWinPos = {rct.left, rct.top};
	SIZE sizeWindow = {rct.right-rct.left, rct.bottom-rct.top};
	int border = (sizeWindow.cx - rcClient.right) / 2;
	POINT ptClientPos = {border, sizeWindow.cy - rcClient.bottom - border};

	HDC hdcScreen = ::GetDC(hwnd);
	HDC hdcMemory = ::CreateCompatibleDC(hdcScreen);
	HBITMAP hBitMap = ::CreateCompatibleBitmap(hdcScreen, sizeWindow.cx, sizeWindow.cy);
	::SelectObject(hdcMemory, hBitMap);
	
	Gdiplus::Graphics graphics(hdcMemory);
	//graphics.SetSmoothingMode(Gdiplus::SmoothingModeHighQuality);
	;
/*
	Gdiplus::Image m_Title(L"toolbarbktop.png");
	graphics.DrawImage(&m_Title, rcClient.left+50, rcClient.top,
	                             m_Title.GetWidth(), m_Title.GetHeight());
	
	Gdiplus::Image m_ToolBK(L"toolbarbkbottom.png");
	graphics.DrawImage(&m_ToolBK, rcClient.left+50, rcClient.top+m_Title.GetHeight()-4,
	                              m_Title.GetWidth(), m_ToolBK.GetHeight());
	
	if (rcTool[0].Width > 24)
	{
		Gdiplus::Image m_Tool0_1(L"intomain_48.png");
		graphics.DrawImage(&m_Tool0_1, rcTool[0]);
	}
	else
	{
		Gdiplus::Image m_Tool0(L"intomain_24.png");
		graphics.DrawImage(&m_Tool0, rcTool[0]);
	}

	if (rcTool[1].Width > 24)
	{
		Gdiplus::Image m_Tool1_1(L"intomini_48.png");
		graphics.DrawImage(&m_Tool1_1, rcTool[1]);
	}
	else
	{
		Gdiplus::Image m_Tool1(L"intomini_24.png");
		graphics.DrawImage(&m_Tool1, rcTool[1]);
	}

	if (rcTool[2].Width > 24)
	{
		Gdiplus::Image m_Tool2_1(L"todolist_48.png");
		graphics.DrawImage(&m_Tool2_1, rcTool[2]);
	}
	else
	{
		Gdiplus::Image m_Tool2(L"todolist_24.png");
		graphics.DrawImage(&m_Tool2, rcTool[2]);
	}
	
	if (rcTool[3].Width > 24)
	{
		Gdiplus::Image m_Tool3_1(L"newevent_big.png");
		graphics.DrawImage(&m_Tool3_1, rcTool[3]);
	}
	else
	{
		Gdiplus::Image m_Tool3(L"mini_newevent_small.png");
		graphics.DrawImage(&m_Tool3, rcTool[3]);
	}
	
	if (rcTool[4].Width > 24)
	{
		Gdiplus::Image m_Tool4_1(L"setting_48.png");
		graphics.DrawImage(&m_Tool4_1, rcTool[4]);
	}
	else
	{
		Gdiplus::Image m_Tool4(L"setting_24.png");
		graphics.DrawImage(&m_Tool4, rcTool[4]);
	}
	
	if (rcTool[5].Width > 24)
	{
		Gdiplus::Image m_Tool5_1(L"exit_48.png");
		graphics.DrawImage(&m_Tool5_1, rcTool[5]);
	}
	else
	{
		Gdiplus::Image m_Tool5(L"exit_24.png");
		graphics.DrawImage(&m_Tool5, rcTool[5]);
	}
*/
	Gdiplus::SolidBrush window_brush(0x40FF8080);
	//window_pen.SetAlignment(Gdiplus::PenAlignmentInset);
	graphics.FillRectangle(&window_brush, 0, 0, sizeWindow.cx, sizeWindow.cy);

	graphics.SetCompositingMode(Gdiplus::CompositingModeSourceCopy);
	Gdiplus::SolidBrush cell_brush(0x80202080);
	Gdiplus::REAL half_shift = row.offset / 2.0f;
	for (int i=0; i < ITEMS; i++)
	{
		Cell& cell = row.cells[i];
		Gdiplus::REAL cell_size = (PICSIZE+BORDERSIZE) * cell.magnification;
		Gdiplus::REAL icon_size = cell_size - BORDERSIZE;
		Gdiplus::REAL diff = cell_size - (PICSIZE+BORDERSIZE);
		Gdiplus::REAL center = cell.center + diff / 2.0f - half_shift;
		graphics.FillRectangle(&cell_brush,
					row.left + center - icon_size / 2.0f, 0.0f,
					icon_size, icon_size);
		half_shift -= diff;
	}
	graphics.SetCompositingMode(Gdiplus::CompositingModeSourceOver);

	Gdiplus::Pen debug_cell_pen(0xFFFF0000);
	for (int i=0; i < ITEMS; i++)
	{
		Cell& cell = row.cells[i];
		Gdiplus::REAL x = row.left + cell.center - (PICSIZE+BORDERSIZE) / 2.0f;
		graphics.DrawRectangle(&debug_cell_pen,
					x, 0.0f,
					(float)(PICSIZE+BORDERSIZE), (float)(PICSIZE+BORDERSIZE/2));
	}

	POINT ptSrc = {0, 0};
	BOOL bRet = ::UpdateLayeredWindow(hwnd, hdcScreen, &ptWinPos, &sizeWindow,
	                                  hdcMemory, &ptSrc, 0, &g_Blend, 2);
	graphics.ReleaseHDC(hdcMemory);
	::ReleaseDC(hwnd, hdcScreen);
	::DeleteObject(hBitMap);
	::DeleteDC(hdcMemory);
}


int GetMoreInt(int x, int nBack)
{
	int ret = 0;
	BOOL bJian = FALSE;

	if (x < 0)
	{
		x = -x;
		bJian = TRUE;
	}

	if (x>=0 && x<(nBack/6))
	{
		ret = 2;
	}
	else if ((x >= (nBack/6)) && (x < (2*nBack/6)))
	{
		ret = 4;
	}
	else if ((x >= (2*nBack/6)) && (x < (3*nBack/6)))
	{
		ret = 6;
	}
	else if ((x >= (3*nBack/6)) && (x < (4*nBack/6)))
	{
		ret = 8;
	}
	else if ((x >= (4*nBack/6)) && (x < (5*nBack/6)))
	{
		ret = 10;
	}
	else if ((x >= (5*nBack/6)) && (x < (6*nBack/6)))
	{
		ret = 12;
	}
	else if (x >= (6*nBack/6))
	{
		ret = 12;
	}

	if (bJian)
	{
		ret = - ret;
	}

	return ret;
}


LRESULT OnCreate(HWND hwnd)
{
	RECT r;
	::GetWindowRect(hwnd, &r);
	::MoveWindow(hwnd,
	             1280/2 - (int)((PICSIZE+BORDERSIZE) * ITEMS + MAX_OFFSET)/2
				 , 0,
	             (int)((PICSIZE+BORDERSIZE) * ITEMS + MAX_OFFSET),
				 (int)((PICSIZE+BORDERSIZE) * SCALE - BORDERSIZE),
	             FALSE);

	row.left = MAX_OFFSET/2;
	for (int i=0; i < ITEMS; i++)
	{
		Cell& cell = row.cells[i];
		cell.center = (PICSIZE+BORDERSIZE) * i + (PICSIZE+BORDERSIZE) / 2;
		cell.magnification = 1.0f;
	}
	row.offset = 0.0f;

	DrawTXBar(hwnd);

	return 0;
}


void OnMouseMove(HWND hwnd, UINT nFlags, POINTS point)
{
	if (point.x < row.left || point.x > row.left + (PICSIZE+BORDERSIZE)*ITEMS)
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
		float distance = (float)abs(row.left + cell.center - point.x);

		// magnification is scaled from 1.0f (no magnification) to SCALE (full magnification)
		if (distance > CURSOR_RADIUS)
			cell.magnification = 1.0f;
		else
		{
			cell.magnification = 1.0f + (SCALE - 1.0f) * (1.0f - distance / CURSOR_RADIUS);
			if (point.x < row.left + CURSOR_RADIUS)
			{
				float real_size = (PICSIZE+BORDERSIZE) * cell.magnification;
				row.offset += (real_size - (PICSIZE+BORDERSIZE))*2;
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
	POINT pt;
	::GetCursorPos(&pt);
	::ScreenToClient(hwnd, &pt);

	for (int i=0; i<6; i++)
	{
		if (::PtInRect(&(rcRange[i]), pt))
			return;
	}
	
	::KillTimer(hwnd, 1);

	rcTool[0].X = 59;
	rcTool[0].Y = 45;
	rcTool[0].Width = 24;
	rcTool[0].Height = 24;
	
	rcTool[1].X = 95;
	rcTool[1].Y = 45;
	rcTool[1].Width = 24;
	rcTool[1].Height = 24;
	
	rcTool[2].X = 131;
	rcTool[2].Y = 45;
	rcTool[2].Width = 24;
	rcTool[2].Height = 24;
	
	rcTool[3].X = 167;
	rcTool[3].Y = 45;
	rcTool[3].Width = 24;
	rcTool[3].Height = 24;
	
	rcTool[4].X = 203;
	rcTool[4].Y = 45;
	rcTool[4].Width = 24;
	rcTool[4].Height = 24;
	
	rcTool[5].X = 239;
	rcTool[5].Y = 45;
	rcTool[5].Width = 24;
	rcTool[5].Height = 24;

	for (int k=0; k<6; k++)
	{
		rcRange[k].left = 53+k*36;
		rcRange[k].top = 40;
		rcRange[k].right = 53+(k+1)*36;
		rcRange[k].bottom = 45+5+5+24;
	}

	DrawTXBar(hwnd);
}


LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	switch (message)
	{
	case WM_CREATE:
		return OnCreate(hWnd);

	case WM_MOUSEMOVE:
		OnMouseMove(hWnd, wParam, MAKEPOINTS(lParam));
		break;

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
