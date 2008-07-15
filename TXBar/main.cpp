#include "stdafx.h"

#define SCALE 2.0f
#define PICSIZE 24
#define BORDERSIZE 12

#define CURSOR_RADIUS ((PICSIZE+BORDERSIZE)*2)
#define ROWPADDING (CURSOR_RADIUS - (PICSIZE+BORDERSIZE)/2)

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
	int pos;
	Cell cells[6];
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
	graphics.SetSmoothingMode(Gdiplus::SmoothingModeHighQuality);
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
	Gdiplus::SolidBrush window_brush(0x60FF0000);
	//window_pen.SetAlignment(Gdiplus::PenAlignmentInset);
	graphics.FillRectangle(&window_brush, 0, 0, sizeWindow.cx, sizeWindow.cy);

	Gdiplus::SolidBrush cell_brush(0x800000FF);
	Gdiplus::REAL shift = row.offset / 2.0f;
	for (int i=0; i < 6; i++)
	{
		Cell& cell = row.cells[i];
		Gdiplus::REAL cell_size = (PICSIZE+BORDERSIZE) * cell.magnification;
		Gdiplus::REAL icon_size = cell_size - BORDERSIZE;
		Gdiplus::REAL center = cell.center + (cell_size - (PICSIZE+BORDERSIZE)) / 2.0f - shift;
		graphics.FillRectangle(&cell_brush,
					row.pos + center - icon_size / 2.0f, 0.0f,
					icon_size, icon_size);
		shift -= cell_size - (PICSIZE+BORDERSIZE);
	}

	Gdiplus::Pen debug_cell_pen(0xFFFF0000);
	for (int i=0; i < 6; i++)
	{
		Cell& cell = row.cells[i];
		Gdiplus::REAL x = row.pos + cell.center - (PICSIZE+BORDERSIZE) / 2.0f;
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


BOOL OnCreate(HWND hwnd)
{
/*
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

	rcBack[0].X = 59;
	rcBack[0].Y = 45;
	rcBack[0].Width = 24;
	rcBack[0].Height = 24;
	
	rcBack[1].X = 95;
	rcBack[1].Y = 45;
	rcBack[1].Width = 24;
	rcBack[1].Height = 24;
	
	rcBack[2].X = 131;
	rcBack[2].Y = 45;
	rcBack[2].Width = 24;
	rcBack[2].Height = 24;
	
	rcBack[3].X = 167;
	rcBack[3].Y = 45;
	rcBack[3].Width = 24;
	rcBack[3].Height = 24;
	
	rcBack[4].X = 203;
	rcBack[4].Y = 45;
	rcBack[4].Width = 24;
	rcBack[4].Height = 24;
	
	rcBack[5].X = 239;
	rcBack[5].Y = 45;
	rcBack[5].Width = 24;
	rcBack[5].Height = 24;

	for (int i=0; i<6; i++)
	{
		rcRange[i].left = 53+i*36;
		rcRange[i].top = 40;
		rcRange[i].right = 53+(i+1)*36;
		rcRange[i].bottom = 45+5+5+24;
	}
*/

//---------------------------------------------------------------
	RECT r;
	::GetWindowRect(hwnd, &r);
	::MoveWindow(hwnd,
	             r.left, r.top,
	             (int)((PICSIZE+BORDERSIZE) * 6 + ROWPADDING * 2), (int)((PICSIZE+BORDERSIZE) * SCALE - BORDERSIZE),
	             FALSE);

	row.pos = ROWPADDING;
	for (int i=0; i < 6; i++)
	{
		Cell& cell = row.cells[i];
		cell.center = (PICSIZE+BORDERSIZE) * i + (PICSIZE+BORDERSIZE) / 2;
		cell.magnification = 1.0f;
	}
	row.offset = 0.0f;

	DrawTXBar(hwnd);

	return TRUE;  // return TRUE  unless you set the focus to a control
}


void OnMouseMove(HWND hwnd, UINT nFlags, POINTS point)
{
/*
	POINT pt = {point.x, point.y};
	int nBack;
	for (int i=0; i<6; i++)
	{
		if (::PtInRect(&(rcRange[i]), pt))
		{
			rcTool[i].X = rcBack[i].X + rcBack[i].Width/2 - 24 + ((rcBack[i].X + rcBack[i].Width/2) - point.x);
			rcTool[i].Y = rcBack[i].Y;	
			rcTool[i].Width = 48;
			rcTool[i].Height = 48;

			nBack = (rcRange[i].right - rcRange[i].left)/2;
				
			rcRange[i].left = rcTool[i].X - 12;
			rcRange[i].top = rcTool[i].Y;
			rcRange[i].right = rcTool[i].X - 12+72;
			rcRange[i].bottom = rcTool[i].Y+53;

			int nLen = 66;
			int x = point.x - (rcTool[i].X+24);

			int nN = GetMoreInt(x, 36);
	
			for (int m=i+1;m<6;m++)
			{
				rcTool[m].X = rcTool[i].X+nLen;
				rcTool[m].Y = rcTool[m].Y;
				if ((m-i) == 1)
				{
					rcTool[m].Width = 36+nN;
					rcTool[m].Height = 36+nN;

					nLen += rcTool[m].Width+12;

				}
				else if ((m-i) == 2)
				{
					if ((24+nN)>24)
					{
						rcTool[m].Width = 24+nN;
						rcTool[m].Height = 24+nN;
					}
					else
					{
						rcTool[m].Width = 24;
						rcTool[m].Height = 24;
					}
					
					nLen += rcTool[m].Width +12;
				}
				else
				{
					rcTool[m].Width = 24;
					rcTool[m].Height = 24;

					nLen += 24+12;
				}

				rcRange[m].left = rcTool[m].X - 6;
				rcRange[m].top = rcTool[m].Y-5;
				rcRange[m].right = rcTool[m].X + rcTool[m].Width+6;
				rcRange[m].bottom = rcTool[m].Y+ rcTool[m].Height +5;
			}
			
			nLen = 0;
			for (int k=i; k>=0; k--)
			{
				if (k != i)
				{				
				if ((i-k) == 1)
				{
					rcTool[k].Width = 36-nN;
					rcTool[k].Height = 36-nN;
					
					nLen += rcTool[k].Width+18;
					
				}
				else if ((i-k) == 2)
				{
					if ((24-nN)>24)
					{
						rcTool[k].Width = 24-nN;
						rcTool[k].Height = 24-nN;
					}
					else
					{
						rcTool[k].Width = 24;
						rcTool[k].Height = 24;
					}
										
					nLen += rcTool[k].Width +12;
				}
				else
				{
					rcTool[k].Width = 24;
					rcTool[k].Height = 24;
					
					nLen += 24+12;
				}
				
				rcTool[k].X = rcTool[i].X - nLen;
				rcTool[k].Y = rcTool[k].Y;

				rcRange[k].left = rcTool[k].X - 6;
				rcRange[k].top = rcTool[k].Y - 5;
				rcRange[k].right = rcTool[k].X + rcTool[k].Width + 6;
				rcRange[k].bottom = rcTool[k].Y+ rcTool[k].Height + 5;
				}
			}

			DrawTXBar(hwnd);
			::SetTimer(hwnd, 1, 10, NULL);
			break;
		}
	}
*/
	//if (point.x - row.pos > (PICSIZE+BORDERSIZE) * 6 - (PICSIZE+BORDERSIZE)/2 || point.y > PICSIZE)
	//	return;

	row.offset = 0.0f;
	for (int i=0; i < 6; i++)
	{
		Cell& cell = row.cells[i];
		float distance = (float)abs(row.pos + cell.center - point.x);

		// magnification is scaled from 1.0f (no magnification) to SCALE (full magnification)
		if (distance > CURSOR_RADIUS)
			cell.magnification = 1.0f;
		else
		{
			cell.magnification = 1.0f + (SCALE - 1.0f) * (1.0f - distance / CURSOR_RADIUS);
			float real_size = (PICSIZE+BORDERSIZE) * cell.magnification;
			float diff = real_size - (PICSIZE+BORDERSIZE);
			row.offset += diff;
			if (distance < (PICSIZE+BORDERSIZE)/2)
			{
				float k = distance * 2.0f / (PICSIZE+BORDERSIZE);
				float x = real_size * k - distance * 2.0f;
				//wtf?
			}
		}
	}

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
		OnCreate(hWnd);
		break;

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
