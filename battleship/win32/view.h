#pragma once

#include "../game/board.h"

HWND CreateMapWidget(HWND hWndParent);
void SetMapWidgetData(HWND hwnd, const std::vector<board::Ship>& ships);

// notifications
#define BSN_FIRST                   WM_USER
#define BSN_SQUARESELECTED			BSN_FIRST+1

/*
class MapWidget
{
	MapWidget(HWND hWndParent)
	  : m_mapBitmap (gridWidth, gridWidth)
	  , m_radarBitmap (gridWidth, gridWidth)
	{
		if (NULL == m_registredClass)
			StaticInit();

		m_hwnd = ::CreateWindow(m_registredClass,
			_T(""),
			WS_CHILD|WS_VISIBLE,
			0,0,0,0,
			hWndParent,
			NULL,
			::GetModuleHandle(NULL),
			NULL);

		m_mapGraphics = Graphics::FromImage(&m_mapBitmap);
		m_radarGraphics = Graphics::FromImage(&m_radarBitmap);

		// temp
		board::Ship ship;
		ship.segments.push_back(board::ShipSegment(2,1));
		ship.segments.push_back(board::ShipSegment(2,2));
		m_mapShips.push_back(ship);
		ship.segments.clear();
		ship.segments.push_back(board::ShipSegment(4,2));
		ship.segments.push_back(board::ShipSegment(5,2));
		ship.segments.push_back(board::ShipSegment(6,2));
		ship.segments[1].active = false;
		ship.segments[2].active = false;
		m_mapShips.push_back(ship);
	}

	~MapWidget()
	{
	}

private:
	void StaticInit()
	{
		// Initialize GDI+.
		ULONG_PTR gdiplusToken;
		GdiplusStartupInput gdiplusStartupInput;
		GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);
		// register class
		WNDCLASS wc;
		memset(&wc, 0, sizeof(wc));
		wc.lpszClassName = _T("MapWidget");
		wc.lpfnWndProc = &WndProc;
		wc.hInstance = ::GetModuleHandle(NULL);
		wc.hCursor = ::LoadCursor(NULL, IDC_ARROW);
		//wc.hbrBackground = ::GetStockObject(WHITE_BRUSH);
		ATOM res = ::RegisterClass(&wc);
		assert (0 != res);
		m_registredClass = (LPCTSTR)MAKELONG(res, 0);
	}

	static LRESULT CALLBACK WndProc(
						HWND hwnd,        // handle to window
						UINT uMsg,        // message identifier
						WPARAM wParam,    // first message parameter
						LPARAM lParam)    // second message parameter
	{
		MapWidget* pthis = (MapWidget*)GetWindowLongPtr(hwnd, 0);

		switch (uMsg)
		{
		case WM_NCCREATE:
			//pthis = new BattleshipView(hwnd);
			pthis = (MapWidget*)((LPCREATESTRUCT)lParam)->lpCreateParams;
			SetWindowLongPtr(hwnd, 0, (LONG)pthis);
			return TRUE;

		case WM_NCDESTROY:
			//delete pthis;
			return 0;

		case WM_PAINT:
			return pthis->OnPaint();

		default:
			break;
		}

		return DefWindowProc(hwnd, uMsg, wParam, lParam);
		return 0; 
	}

	LONG OnPaint()
	{
		PAINTSTRUCT ps; 
		HDC hdc = BeginPaint(m_hwnd, &ps); 

		Graphics graphics(hdc);

		draw_map_grid(m_mapGraphics, m_mapShips);
		//draw_radar_grid(hdc);
		graphics.DrawImage(&m_mapBitmap, 0, 0, m_mapBitmap.GetWidth(), m_mapBitmap.GetHeight());

		EndPaint(m_hwnd, &ps); 
		return 0;
	}

	HWND m_hwnd;
	static LPCTSTR m_registredClass;

	Graphics* m_mapGraphics;
	Bitmap m_mapBitmap;
	Graphics* m_radarGraphics;
	Bitmap m_radarBitmap;
	// drawing state
	void* m_radarShips;
	void* m_radarShots;
	bool m_radarShotActive;
	std::vector<board::Ship> m_mapShips;
	void* m_mapShots;
	bool m_mapShotActive;
};
*/
