
#define WIN32_LEAN_AND_MEAN  // Exclude rarely-used stuff from Windows headers

// Windows Header Files:
#include <windows.h>

// C/C++ RunTime Header Files
#include <assert.h>


#include "hooks.h"


HINSTANCE g_hModule = NULL;
/*
As stated in MSDN, the WH_MOUSE_LL (and WH_KEYBOARD_LL) hooks are not injected
into another process. Instead, the context switches back to the process that
installed the hook and it is called in its original context.
So it is ok to use global variables in LowLevelKeyboardProc and
LowLevelMouseProc.
*/
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
		if (g_llmouse_hwnd != NULL)
			clearLLMouseHook(g_llmouse_hhook);
		break;

	//case DLL_THREAD_ATTACH:
	//case DLL_THREAD_DETACH:
	}
	return TRUE;
}



LRESULT CALLBACK LowLevelMouseProc(int nCode, WPARAM wParam, LPARAM lParam)
{
	assert (g_llmouse_hwnd != NULL);
	HHOOK llmouse_hhook = g_llmouse_hhook;

	if (nCode < 0)
		return ::CallNextHookEx(NULL, nCode, wParam, lParam);

	if (nCode == HC_ACTION && wParam == WM_MOUSEMOVE)
	{
		MSLLHOOKSTRUCT* mouse_data = reinterpret_cast<MSLLHOOKSTRUCT*>(lParam);
		RECT rc;
		::GetWindowRect(g_llmouse_hwnd, &rc);
		POINT pt = mouse_data->pt;
		::ScreenToClient(g_llmouse_hwnd, &pt);
		int mousemove_flag = ::PtInRect(&rc, mouse_data->pt) ? MM_IN : MM_OUT;
		::PostMessage(g_llmouse_hwnd, WM_MOUSEMOVE_GLOBAL,
				mousemove_flag, MAKELPARAM(pt.x, pt.y));
	}

	return ::CallNextHookEx(llmouse_hhook, nCode, wParam, lParam);
}


__declspec(dllexport)
HHOOK setLLMouseHook(HWND hWnd)
{
	assert (g_llmouse_hwnd == NULL);
	assert (g_llmouse_hhook == NULL);

	g_llmouse_hhook = ::SetWindowsHookEx(WH_MOUSE_LL, &LowLevelMouseProc, g_hModule, 0);
	if (g_llmouse_hhook == NULL)
		return NULL;

	g_llmouse_hwnd = hWnd;
	return g_llmouse_hhook;
}


__declspec(dllexport)
BOOL clearLLMouseHook(HHOOK hhook)
{
	assert (g_llmouse_hwnd != NULL);
	assert (g_llmouse_hhook != NULL);
	assert (g_llmouse_hhook == hhook);

	if (0 == ::UnhookWindowsHookEx(g_llmouse_hhook))
		return FALSE;

	g_llmouse_hhook = NULL;
	g_llmouse_hwnd = NULL;
	return TRUE;
}
