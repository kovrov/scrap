#include "stdafx.h"
#include "view.h"



class BattleshipView
{
public:
	BattleshipView(HWND hwnd) { m_hwnd = hwnd; }
	~BattleshipView(void) {}
	LONG OnPaint()
	{
		PAINTSTRUCT ps; 
		HDC hdc; 
		RECT rc; 
		POINT aptStar[6] = {50,2, 2,98, 98,33, 2,33, 98,98, 50,2}; 

		hdc = BeginPaint(m_hwnd, &ps); 
		GetClientRect(m_hwnd, &rc); 
		SetMapMode(hdc, MM_ANISOTROPIC); 
		SetWindowExtEx(hdc, 100, 100, NULL); 
		SetViewportExtEx(hdc, rc.right, rc.bottom, NULL); 
		Polyline(hdc, aptStar, 6); 
		EndPaint(m_hwnd, &ps); 
		return 0;
	}
private:
	HWND m_hwnd;
};





BOOL InitView()
{
	WNDCLASSEX	wcx;
	memset(&wcx, 0, sizeof(wcx));
	wcx.cbSize        = sizeof(wcx);
	wcx.lpfnWndProc   = &ViewWndProc;
	wcx.cbWndExtra    = sizeof(void*);
	wcx.hInstance     = GetModuleHandle(NULL);
	//wcx.hCursor       = LoadCursor(NULL, IDC_ARROW);
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
