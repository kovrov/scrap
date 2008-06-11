// battleship.cpp : Defines the entry point for the application.
//

#include "stdafx.h"
#include "battleship.h"
#include "view.h"
#include <assert.h>

#define MAX_LOADSTRING 100

// Global Variables:
HINSTANCE hInst;								// current instance
TCHAR szTitle[MAX_LOADSTRING];					// The title bar text
TCHAR szWindowClass[MAX_LOADSTRING];			// the main window class name
HWND hwndView;

// Forward declarations of functions included in this code module:
ATOM				RegisterMainWindowClass(HINSTANCE hInstance);
BOOL				InitInstance(HINSTANCE, int);
LRESULT CALLBACK	WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK	About(HWND, UINT, WPARAM, LPARAM);

int APIENTRY _tWinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPTSTR    lpCmdLine,
                     int       nCmdShow)
{
	UNREFERENCED_PARAMETER(hPrevInstance);
	UNREFERENCED_PARAMETER(lpCmdLine);

 	// TODO: Place code here.
	MSG msg;
	HACCEL hAccelTable;

	// Initialize global strings
	LoadString(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
	LoadString(hInstance, IDC_BATTLESHIP, szWindowClass, MAX_LOADSTRING);
	RegisterMainWindowClass(hInstance);

	// Perform application initialization:
	if (!InitInstance(hInstance, nCmdShow))
		return FALSE;

	hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_BATTLESHIP));

	// Main message loop:
	while (GetMessage(&msg, NULL, 0, 0))
	{
		if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
		{
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
	}

	return (int) msg.wParam;
}



ATOM RegisterMainWindowClass(HINSTANCE hInstance)
{
	WNDCLASSEX wcex;

	wcex.cbSize = sizeof(WNDCLASSEX);

	wcex.style			= CS_HREDRAW | CS_VREDRAW;
	wcex.lpfnWndProc	= &WndProc;
	wcex.cbClsExtra		= 0;
	wcex.cbWndExtra		= 0;
	wcex.hInstance		= hInstance;
	wcex.hIcon			= LoadIcon(hInstance, MAKEINTRESOURCE(IDI_BATTLESHIP));
	wcex.hCursor		= LoadCursor(NULL, IDC_ARROW);
	wcex.hbrBackground	= (HBRUSH)(NULL); // no background
	wcex.lpszMenuName	= MAKEINTRESOURCE(IDC_BATTLESHIP);
	wcex.lpszClassName	= szWindowClass;
	wcex.hIconSm		= LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

	return RegisterClassEx(&wcex);
}


BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
   HWND hWnd;

   hInst = hInstance; // Store instance handle in our global variable

   hWnd = CreateWindow(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW,
      CW_USEDEFAULT, 0, CW_USEDEFAULT, 0, NULL, NULL, hInstance, NULL);

   assert (hWnd);

   ::SetWindowPos(hWnd, NULL,0,0,0,0, SWP_NOMOVE|SWP_NOZORDER);  // hack to update MINMAXINFO

   ::ShowWindow(hWnd, nCmdShow);
   ::UpdateWindow(hWnd);

   return TRUE;
}


LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	int wmId, wmEvent;

	switch (message)
	{
	case WM_COMMAND:
		wmId    = LOWORD(wParam);
		wmEvent = HIWORD(wParam);
		// Parse the menu selections:
		switch (wmId)
		{
		case IDM_ABOUT:
			::DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
			break;

		case IDM_EXIT:
			::DestroyWindow(hWnd);
			break;

		case IDM_NEWGAME:
			assert (false);
			break;

		default:
			return ::DefWindowProc(hWnd, message, wParam, lParam);
		}
		break;

	case WM_NOTIFY:
		switch (reinterpret_cast<NMHDR*>(lParam)->code )
		{
		case BSN_SQUARESELECTED:
			{
			BSNSquareInfo* si = reinterpret_cast<BSNSquareInfo*>(lParam);
			si->pos;
			}
			break; 
		}
		break; 

	case WM_CREATE:
		hwndView = CreateMapWidget(hWnd);
		assert (hwndView);
		// temp
		{
		std::vector<board::Ship> ships;
		board::Ship ship;
		ship.segments.push_back(board::ShipSegment(2,1));
		ship.segments.push_back(board::ShipSegment(2,2));
		ships.push_back(ship);
		ship.segments.clear();
		ship.segments.push_back(board::ShipSegment(4,2));
		ship.segments.push_back(board::ShipSegment(5,2));
		ship.segments.push_back(board::ShipSegment(6,2));
		ship.segments[1].active = false;
		ship.segments[2].active = false;
		ships.push_back(ship);
		SetMapWidgetData(hwndView, ships);
		}
		return 0;

	case WM_DESTROY:
		::PostQuitMessage(0);
		break;

	case WM_SIZE:
		::MoveWindow(hwndView, 0, 0, LOWORD(lParam), HIWORD(lParam), TRUE);
		return 0;

	case WM_GETMINMAXINFO:
		{
		RECT rect;
		if (::GetClientRect(hwndView, &rect))
		{
			int menu_y = ::GetSystemMetrics(SM_CYMENU);
			int frame_y = ::GetSystemMetrics(SM_CYSIZEFRAME);
			int frame_x = ::GetSystemMetrics(SM_CXSIZEFRAME);
			int caption_y = ::GetSystemMetrics(SM_CYCAPTION);
			MINMAXINFO* minmaxinfo = (MINMAXINFO*)lParam;
			minmaxinfo->ptMaxTrackSize.x = minmaxinfo->ptMinTrackSize.x = rect.right + frame_x*2;
			minmaxinfo->ptMaxTrackSize.y = minmaxinfo->ptMinTrackSize.y = rect.bottom + frame_y*2 + menu_y + caption_y;
			minmaxinfo = NULL;
		}
		}
		return 0;

	default:
		return ::DefWindowProc(hWnd, message, wParam, lParam);
	}
	return 0;
}


// Message handler for about box.
INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
	UNREFERENCED_PARAMETER(lParam);
	switch (message)
	{
	case WM_INITDIALOG:
		return (INT_PTR)TRUE;

	case WM_COMMAND:
		if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
		{
			EndDialog(hDlg, LOWORD(wParam));
			return (INT_PTR)TRUE;
		}
		break;
	}
	return (INT_PTR)FALSE;
}
