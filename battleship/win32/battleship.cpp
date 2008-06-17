// battleship.cpp : Defines the entry point for the application.
//

#include "stdafx.h"
#include "battleship.h"
#include "view.h"
#include <assert.h>
#include <cstdlib>

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
HWND hwndMapView = NULL;
HWND hwndRadarView = NULL;
HWND hwndMain = NULL;

DWORD g_worker_thread_id = 0;

#define MSG_GAME_STATE_CHANGED WM_APP+0
#define MSG_USER_INPUT         WM_APP+1

enum { UI_PLAYERMOVE, UI_NEWGAME, UI_QUIT };


void on_new_game()
{
	::PostThreadMessage(g_worker_thread_id, MSG_USER_INPUT, UI_NEWGAME, 0);
}

DWORD WINAPI game_thread(LPVOID lpParameter)
{
	logic::PLAYER_HANDLE player = 0;
	logic::PLAYER_HANDLE opponent = 1;
	logic::Game game(player, opponent);
	std::map<logic::PLAYER_HANDLE, ai::ComputerPlayer> players;

	srand((unsigned)time(NULL));

	MSG msg;
	while (::GetMessage(&msg, NULL, 0, 0))
	{
		if (MSG_GAME_STATE_CHANGED == msg.message)
		{
			switch (game.GetState())
			{
			case logic::BATTLE_STARTED:
				// temp
				assert (logic::BATTLE_STARTED == game.GetState());
				// setup ships
				game.Setup(player, ai::setup_ships(10, game.GetConfig()));
				game.Setup(opponent, ai::setup_ships(10, game.GetConfig()));

				// HACK!!! TODO: implement state change notification in game library
				::PostThreadMessage(g_worker_thread_id, MSG_GAME_STATE_CHANGED, 0, 0);

				// reset state
				players[player] = ai::ComputerPlayer(10, game.GetConfig());
				players[opponent] = ai::ComputerPlayer(10, game.GetConfig());
				break;

			case logic::PLAYER_TURN: {
				// update widget
				SetMapWidgetData(hwndMapView, &game.GetPlayerShips(player), &game.GetPlayerShots(opponent));
				SetMapWidgetData(hwndRadarView, &game.GetPlayerShips(opponent), &game.GetPlayerShots(player));
				logic::PLAYER_HANDLE current_player_id = game.GetCurrentPlayer();

				//if (current_player_id == opponent)
					::Sleep(1000);
				
				ai::ComputerPlayer& current_player = players[current_player_id];
				board::Pos shot = current_player.Shot();
				board::SHOT res = game.Shoot(current_player_id, shot);

				// HACK!!! TODO: implement state change notification in game library
				::PostThreadMessage(g_worker_thread_id, MSG_GAME_STATE_CHANGED, 0, 0);

				current_player.Track(shot, res);
				} break;

			case logic::BATTLE_ENDED:
				// update widget
				SetMapWidgetData(hwndMapView, &game.GetPlayerShips(player), &game.GetPlayerShots(opponent));
				SetMapWidgetData(hwndRadarView, &game.GetPlayerShips(opponent), &game.GetPlayerShots(player));
				//printf("%d win, shots made: %d\n", game.GetCurrentPlayer(), shots_made[game.GetCurrentPlayer()]);
				break;
			}
		}
		else if (MSG_USER_INPUT == msg.message)
		{
			if (UI_PLAYERMOVE == msg.wParam)
			{
				if (game.GetState() == logic::PLAYER_TURN && game.GetCurrentPlayer() == player)
				{
					board::SHOT res = game.Shoot(player, board::Pos(LOWORD(msg.lParam), HIWORD(msg.lParam)));
					// HACK!!! TODO: implement state change notification in game library
					::PostThreadMessage(g_worker_thread_id, MSG_GAME_STATE_CHANGED, 0, 0);
				}
			}
			else if (UI_NEWGAME == msg.wParam)
			{
				// HACK!!! TODO: implement state change notification in game library
				::PostThreadMessage(g_worker_thread_id, MSG_GAME_STATE_CHANGED, 0, 0);
			}
		}
	}
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

	HANDLE hgame = ::CreateThread(NULL, 0, &game_thread, NULL, 0, &g_worker_thread_id);

	// Main message loop:
	while (::GetMessage(&msg, NULL, 0, 0))
	{
		if (!::TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
		{
			::TranslateMessage(&msg);
			::DispatchMessage(&msg);
		}
	}

	::TerminateThread(hgame, 0);

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
			::PostThreadMessage(g_worker_thread_id, MSG_USER_INPUT, UI_PLAYERMOVE, MAKELPARAM(si->pos.x, si->pos.y));
		}
		break; 

	case WM_CREATE:
		hwndMapView = CreateMapWidget(hWnd);
		assert (hwndMapView);
		hwndRadarView = CreateMapWidget(hWnd);
		assert (hwndRadarView);
		break;

	case WM_DESTROY:
		::PostQuitMessage(0);
		break;

	case WM_SIZE: {
		int width = LOWORD(lParam);
		int height = HIWORD(lParam);
		::MoveWindow(hwndMapView, 0, 0, width, height, TRUE);
		RECT rect;
		::GetClientRect(hwndMapView, &rect);
		::MoveWindow(hwndRadarView, rect.right, 0, width, height, TRUE);
		} return 0;

	case WM_GETMINMAXINFO: {
		RECT rect;
		if (::GetClientRect(hwndMapView, &rect))
		{
			int menu_y = ::GetSystemMetrics(SM_CYMENU);
			int frame_y = ::GetSystemMetrics(SM_CYFIXEDFRAME); // SM_CYSIZEFRAME
			int frame_x = ::GetSystemMetrics(SM_CXFIXEDFRAME); // SM_CXSIZEFRAME
			int caption_y = ::GetSystemMetrics(SM_CYCAPTION);
			MINMAXINFO* minmaxinfo = reinterpret_cast<MINMAXINFO*>(lParam);

			minmaxinfo->ptMinTrackSize.x = rect.right + frame_x*2;
			minmaxinfo->ptMinTrackSize.y = rect.bottom + frame_y*2 + menu_y + caption_y;
			// temp hack
			minmaxinfo->ptMinTrackSize.x += rect.right;

			minmaxinfo->ptMaxTrackSize.x = minmaxinfo->ptMinTrackSize.x;
			minmaxinfo->ptMaxTrackSize.y = minmaxinfo->ptMinTrackSize.y;
		}
	}	break;

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
