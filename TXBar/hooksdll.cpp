
#define WIN32_LEAN_AND_MEAN  // Exclude rarely-used stuff from Windows headers

// Windows Header Files:
#include <windows.h>

// C/C++ RunTime Header Files
#include <assert.h>


#include "hooks.h"


HINSTANCE g_hModule = NULL;
//HWND  g_mouse_hwnd = NULL;
//HHOOK g_mouse_hhook = NULL;
HWND  g_llmouse_hwnd = NULL;
HHOOK g_llmouse_hhook = NULL;

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD   ul_reason_for_call,
                       LPVOID  lpReserved)
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		g_hModule = hModule;
		break;

	case DLL_PROCESS_DETACH:
//		if (g_mouse_hwnd != NULL)
//			clearMouseHook(g_mouse_hwnd);
		if (g_llmouse_hwnd != NULL)
			clearLLMouseHook(g_llmouse_hwnd);
		break;

	//case DLL_THREAD_ATTACH:
	//case DLL_THREAD_DETACH:
	}
	return TRUE;
}


/*
LRESULT CALLBACK MouseProc(int nCode, WPARAM wParam, LPARAM lParam)
{
	if (nCode < 0)
		return ::CallNextHookEx(NULL, nCode, wParam, lParam);

	if (nCode == HC_ACTION || nCode == HC_NOREMOVE)
	{
		if (wParam == WM_MOUSEMOVE)
		{
			MOUSEHOOKSTRUCT* mouse_data = reinterpret_cast<MOUSEHOOKSTRUCT*>(lParam);
			::PostMessage(g_mouse_hwnd, WM_MOUSEMOVE,
					0, MAKELPARAM(mouse_data->pt.x+10, mouse_data->pt.y));
		}
	}

	return ::CallNextHookEx(NULL, nCode, wParam, lParam);
}


__declspec(dllexport)
BOOL setMouseHook(HWND hWnd)
{
	assert (g_mouse_hwnd == NULL);
	assert (g_mouse_hhook == NULL);

	g_mouse_hhook = ::SetWindowsHookEx(WH_MOUSE, &MouseProc, g_hModule, 0);
	if (g_mouse_hhook == NULL)
		return FALSE;

	g_mouse_hwnd = hWnd;
	return TRUE;
}


__declspec(dllexport)
BOOL clearMouseHook(HWND hWnd)
{
	assert (g_mouse_hwnd == hWnd);
	assert (g_mouse_hwnd != NULL);
	assert (g_mouse_hhook != NULL);

	if (0 == ::UnhookWindowsHookEx(g_mouse_hhook))
		return FALSE;

	g_mouse_hhook = NULL;
	g_mouse_hwnd = NULL;
	return TRUE;
}
*/


LRESULT CALLBACK LowLevelMouseProc(int nCode, WPARAM wParam, LPARAM lParam)
{
	assert (g_llmouse_hwnd != NULL);

	if (nCode < 0)
		return ::CallNextHookEx(NULL, nCode, wParam, lParam);

	if (nCode == HC_ACTION)
	{
		if (wParam == WM_MOUSEMOVE)
		{
			MSLLHOOKSTRUCT* mouse_data = reinterpret_cast<MSLLHOOKSTRUCT*>(lParam);
			RECT rc;
			::GetWindowRect(g_llmouse_hwnd, &rc);
			if (::PtInRect(&rc, mouse_data->pt))
			{
				::PostMessage(g_llmouse_hwnd, WM_MOUSEMOVE,
						0,
						MAKELPARAM(mouse_data->pt.x - rc.left, mouse_data->pt.y - rc.top));
			}
		}
	}

	return ::CallNextHookEx(NULL, nCode, wParam, lParam);
}


__declspec(dllexport)
BOOL setLLMouseHook(HWND hWnd)
{
	assert (g_llmouse_hwnd == NULL);
	assert (g_llmouse_hhook == NULL);

	g_llmouse_hhook = ::SetWindowsHookEx(WH_MOUSE_LL, &LowLevelMouseProc, g_hModule, 0);
	if (g_llmouse_hhook == NULL)
		return FALSE;

	g_llmouse_hwnd = hWnd;
	return TRUE;
}


__declspec(dllexport)
BOOL clearLLMouseHook(HWND hWnd)
{
	assert (g_llmouse_hwnd == hWnd);
	assert (g_llmouse_hwnd != NULL);
	assert (g_llmouse_hhook != NULL);

	if (0 == ::UnhookWindowsHookEx(g_llmouse_hhook))
		return FALSE;

	g_llmouse_hhook = NULL;
	g_llmouse_hwnd = NULL;
	return TRUE;
}
