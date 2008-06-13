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
board::Pos g_SquareSelected(0,0); // FIXME


void on_new_game()
{
	// HACK!!! TODO: implement state change notification in game library
	::PostMessage(hwndMain, WM_GAME_STATE_CHANGED, 0, 0);
}

DWORD WINAPI worker(LPVOID lpParameter)
{
	logic::PLAYER_HANDLE player = 0;
	logic::PLAYER_HANDLE opponent = 1;
	logic::Game game(player, opponent);
	std::map<logic::PLAYER_HANDLE, ai::ComputerPlayer> players;


	BOOL manual_reset = TRUE;
	g_hEvents[GAME_STATE] = ::CreateEvent(NULL, manual_reset, FALSE, NULL);
	g_hEvents[USER_INPUT] = ::CreateEvent(NULL, manual_reset, FALSE, NULL);
	DWORD nCount = 2;

	while (true)
	{
		DWORD event = ::WaitForMultipleObjects(nCount, g_hEvents, FALSE, INFINITE);

		if (GAME_STATE == event)
		{
			::ResetEvent(g_hEvents[GAME_STATE]);
			switch (game.GetState())
			{
			case logic::BATTLE_STARTED:
				// temp
				assert (logic::BATTLE_STARTED == game.GetState());
				// setup ships
				game.Setup(player, ai::setup_ships(10, game.GetConfig()));
				game.Setup(opponent, ai::setup_ships(10, game.GetConfig()));

				// HACK!!! TODO: implement state change notification in game library
				::PostMessage(hwndMain, WM_GAME_STATE_CHANGED, 0, 0);

				// reset state
				players[player] = ai::ComputerPlayer(10, game.GetConfig());
				players[opponent] = ai::ComputerPlayer(10, game.GetConfig());
				break;

			case logic::PLAYER_TURN: {
				// update widget
				SetMapWidgetData(hwndView, &game.GetPlayerShips(player), &game.GetPlayerShots(opponent));
				logic::PLAYER_HANDLE current_player_id = game.GetCurrentPlayer();

				if (current_player_id == opponent)
					::Sleep(1000);
				
				ai::ComputerPlayer& current_player = players[current_player_id];
				board::Pos shot = current_player.Shot();
				board::SHOT res = game.Shoot(current_player_id, shot);

				// HACK!!! TODO: implement state change notification in game library
				::PostMessage(hwndMain, WM_GAME_STATE_CHANGED, 0, 0);

				current_player.Track(shot, res);
				} break;

			case logic::BATTLE_ENDED:
				// update widget
				SetMapWidgetData(hwndView, &game.GetPlayerShips(player), &game.GetPlayerShots(opponent));
				//printf("%d win, shots made: %d\n", game.GetCurrentPlayer(), shots_made[game.GetCurrentPlayer()]);
				break;
			}
		}
		else if (USER_INPUT == event)
		{
			::ResetEvent(g_hEvents[USER_INPUT]);
			if (game.GetState() == logic::PLAYER_TURN && game.GetCurrentPlayer() == player)
			{
				board::SHOT res = game.Shoot(player, g_SquareSelected);

				// HACK!!! TODO: implement state change notification in game library
				::PostMessage(hwndMain, WM_GAME_STATE_CHANGED, 0, 0);
			}
		}
		else
			break;
	}
	::CloseHandle(g_hEvents[GAME_STATE]);
	::CloseHandle(g_hEvents[USER_INPUT]);
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
	::LoadString(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
	::LoadString(hInstance, IDC_BATTLESHIP, szWindowClass, MAX_LOADSTRING);
	RegisterMainWindowClass(hInstance);

	// Perform application initialization:
	if (!::InitInstance(hInstance, nCmdShow))
		return FALSE;

	hAccelTable = ::LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_BATTLESHIP));

	DWORD ThreadId;
	HANDLE hworker = ::CreateThread(NULL, 0, &worker, g_hEvents, 0, &ThreadId);

	// Main message loop:
	while (::GetMessage(&msg, NULL, 0, 0))
	{
		if (!::TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
		{
			::TranslateMessage(&msg);
			::DispatchMessage(&msg);
		}
	}

	::TerminateThread(hworker, 0);

	return msg.wParam;
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
	wcex.hIcon			= ::LoadIcon(hInstance, MAKEINTRESOURCE(IDI_BATTLESHIP));
	wcex.hCursor		= ::LoadCursor(NULL, IDC_ARROW);
	wcex.hbrBackground	= NULL; // no background
	wcex.lpszMenuName	= MAKEINTRESOURCE(IDC_BATTLESHIP);
	wcex.lpszClassName	= szWindowClass;
	wcex.hIconSm		= ::LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

	return ::RegisterClassEx(&wcex);
}


BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
   hInst = hInstance; // Store instance handle in our global variable

   hwndMain = CreateWindow(szWindowClass, szTitle, WS_OVERLAPPED|WS_CAPTION|WS_SYSMENU|WS_MINIMIZEBOX, // WS_OVERLAPPEDWINDOW
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
			g_SquareSelected = si->pos;
			::SetEvent(g_hEvents[USER_INPUT]);
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
			int frame_y = ::GetSystemMetrics(SM_CYFIXEDFRAME); // SM_CYSIZEFRAME
			int frame_x = ::GetSystemMetrics(SM_CXFIXEDFRAME); // SM_CXSIZEFRAME
			int caption_y = ::GetSystemMetrics(SM_CYCAPTION);
			MINMAXINFO* minmaxinfo = reinterpret_cast<MINMAXINFO*>(lParam);
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
		return TRUE;

	case WM_COMMAND:
		if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
		{
			::EndDialog(hDlg, LOWORD(wParam));
			return TRUE;
		}
		break;
	}
	return FALSE;
}
