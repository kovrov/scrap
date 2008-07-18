#pragma once


#ifdef DLL_EXPORTS
# define LIBSPEC __declspec(dllexport)
#else
# define LIBSPEC __declspec(dllimport)
#endif

extern "C"
{
/*
	LIBSPEC BOOL setMouseHook(HWND hWnd);
	LIBSPEC BOOL clearMouseHook(HWND hWnd);
*/
	LIBSPEC BOOL setLLMouseHook(HWND hWnd);
	LIBSPEC BOOL clearLLMouseHook(HWND hWnd);
}

#undef LIBSPEC
