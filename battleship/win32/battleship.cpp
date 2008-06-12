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
HWND hwndMain;

HANDLE  g_hEvents[2];
// named indexes of events array
#define GAME_STATE 0
#define USER_INPUT 1


void on_new_game()
{
	// HACK!!! TODO: implement state change notification in game library
	::PostMessage(hwndMain, WM_GAME_STATE_CHANGED, 0, 0);
}

DWORD WINAPI worker(LPVOID lpParameter)
{
	HANDLE*  hevents = (HANDLE*)lpParameter;
	// just named references
	HANDLE &hstate     = hevents[0];

	logic::PLAYER_HANDLE PLAYER1 = 0;
	logic::PLAYER_HANDLE PLAYER2 = 1;
	logic::Game game(PLAYER1, PLAYER2);
	std::map<logic::PLAYER_HANDLE, ai::ComputerPlayer> players;

	logic::PLAYER_HANDLE player = PLAYER1;
	logic::PLAYER_HANDLE opponent = PLAYER2;

	BOOL manual_reset = TRUE;
	hstate = ::CreateEvent(NULL, manual_reset, FALSE, NULL);
	while (WAIT_OBJECT_0 == ::WaitForSingleObject(hstate, INFINITE))
	{
		::ResetEvent(hstate);
		switch (game.GetState())
		{
		case logic::BATTLE_STARTED: {
			// temp
			assert (logic::BATTLE_STARTED == game.GetState());
			// setup ships
			game.Setup(PLAYER1, ai::setup_ships(10, game.GetConfig()));
			game.Setup(PLAYER2, ai::setup_ships(10, game.GetConfig()));

			// HACK!!! TODO: implement state change notification in game library
			::PostMessage(hwndMain, WM_GAME_STATE_CHANGED, 0, 0);

			// reset state
			players[PLAYER1] = ai::ComputerPlayer(10, game.GetConfig());
			players[PLAYER2] = ai::ComputerPlayer(10, game.GetConfig());
		}	break;

		case logic::PLAYER_TURN: {
			if (game.GetCurrentPlayer() == opponent)
				::Sleep(1000);
			logic::PLAYER_HANDLE current_player_id = game.GetCurrentPlayer();
			ai::ComputerPlayer& current_player = players[current_player_id];
			board::Pos shot = current_player.Shot();
			board::SHOT res = game.Shoot(current_player_id, shot);

			// HACK!!! TODO: implement state change notification in game library
			::PostMessage(hwndMain, WM_GAME_STATE_CHANGED, 0, 0);

			current_player.Track(shot, res);
		}	break;

		case logic::BATTLE_ENDED:
			//printf("%d win, shots made: %d\n", game.GetCurrentPlayer(), shots_made[game.GetCurrentPlayer()]);
			break;
		}
		// update widget
		SetMapWidgetData(hwndView, &game.GetPlayerShips(player), &game.GetPlayerShots(opponent));
	}
	::CloseHandle(hstate);
	return 0;
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

	DWORD ThreadId;
	HANDLE hworker = ::CreateThread(NULL, 0, &worker, g_hEvents, 0, &ThreadId);

	// Main message loop:
	while (GetMessage(&msg, NULL, 0, 0))
	{
		if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
		{
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
	}

	::TerminateThread(hworker, 0);

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
   hInst = hInstance; // Store instance handle in our global variable

   hwndMain = CreateWindow(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW ^ WS_MAXIMIZEBOX,
      CW_USEDEFAULT, 0, CW_USEDEFAULT, 0, NULL, NULL, hInstance, NULL);

   assert (hwndMain);

   ::SetWindowPos(hwndMain, NULL,0,0,0,0, SWP_NOMOVE|SWP_NOZORDER);  // hack to update MINMAXINFO

   ::ShowWindow(hwndMain, nCmdShow);
   ::UpdateWindow(hwndMain);

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
		if (BSN_SQUARESELECTED == reinterpret_cast<NMHDR*>(lParam)->code)
		{
			BSNSquareInfo* si = reinterpret_cast<BSNSquareInfo*>(lParam);
			si->pos;
		}
		break; 

	case WM_CREATE:
		hwndView = CreateMapWidget(hWnd);
		assert (hwndView);
		break;

	case WM_DESTROY:
		::PostQuitMessage(0);
		break;

	case WM_SIZE:
		::MoveWindow(hwndView, 0, 0, LOWORD(lParam), HIWORD(lParam), TRUE);
		break;

	case WM_GETMINMAXINFO: {
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
	}	break;

	// application specific messages
	case WM_GAME_STATE_CHANGED:
		::SetEvent(g_hEvents[GAME_STATE]);
		break;

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
