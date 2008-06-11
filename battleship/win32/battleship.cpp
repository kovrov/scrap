// battleship.cpp : Defines the entry point for the application.
//

#include "stdafx.h"
#include "battleship.h"
#include "view.h"
#include <assert.h>

// game stuff
#include "../game/logic.h"
#include "../game/ai.h"
#include "../game/board.h"
// support
#include <vector>
#include <map>
#include <exception>
#include <stdlib.h>
#include <time.h>

#define MAX_LOADSTRING 100

// Global Variables:
HINSTANCE hInst;								// current instance
TCHAR szTitle[MAX_LOADSTRING];					// The title bar text
TCHAR szWindowClass[MAX_LOADSTRING];			// the main window class name
HWND hwndView;


// game stuff (temp)
logic::PLAYER_HANDLE g_PLAYER1 = 0;
logic::PLAYER_HANDLE g_PLAYER2 = 1;
logic::Game g_game(g_PLAYER1, g_PLAYER2);
std::map<logic::PLAYER_HANDLE, ai::ComputerPlayer> g_players;
std::map<logic::PLAYER_HANDLE, int> g_shots_made;

void on_new_game() // state == logic::BATTLE_STARTED
{
	// setup ships
	g_game.Setup(g_PLAYER1, ai::setup_ships(10, g_game.GetConfig()));
	g_game.Setup(g_PLAYER2, ai::setup_ships(10, g_game.GetConfig()));
	// reset state
	g_players[g_PLAYER1] = ai::ComputerPlayer(10, g_game.GetConfig());
	g_players[g_PLAYER2] = ai::ComputerPlayer(10, g_game.GetConfig());
	g_shots_made[g_PLAYER1] = g_shots_made[g_PLAYER2] = 0;
	// temp
	assert (logic::PLAYER_TURN == g_game.GetState());
	// update widget
	SetMapWidgetData(hwndView, &g_game.GetPlayerShips(g_PLAYER1));
}

void shot() // state == logic::PLAYER_TURN
{
	logic::PLAYER_HANDLE current_player_id = g_game.GetCurrentPlayer();
	ai::ComputerPlayer& current_player = g_players[current_player_id];
	board::Pos shot = current_player.Shot();
	board::SHOT res = g_game.Shoot(current_player_id, shot);
	current_player.Track(shot, res);
	g_shots_made[current_player_id] += 1;
	//print_sea(g_game, current_player_id, shot, res);
}




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
			on_new_game();
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
