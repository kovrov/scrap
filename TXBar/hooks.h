#pragma once


#define WM_MOUSEMOVE_GLOBAL WM_USER // I'm too lazy to use RegisterWindowMessage...
#define MM_IN 1
#define MM_OUT 2


#ifdef DLL_EXPORTS
# define LIBSPEC __declspec(dllexport)
#else
# define LIBSPEC __declspec(dllimport)
#endif

extern "C"
{
	LIBSPEC HHOOK setLLMouseHook(HWND hWnd);
	LIBSPEC BOOL clearLLMouseHook(HHOOK hhook);
}

#undef LIBSPEC
