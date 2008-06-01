#pragma once

#define VIEW_CLASS _T("ViewClassName")

LRESULT WINAPI ViewWndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam);
BOOL InitView();
