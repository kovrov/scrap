// example1.cpp : Defines the entry point for the application.
//

#include "stdafx.h"
#include "example1.h"

#define MAX_LOADSTRING 100

// Global Variables:
HINSTANCE g_hinst;								// current instance
TCHAR g_title[MAX_LOADSTRING];					// The title bar text
TCHAR g_window_class[MAX_LOADSTRING];			// the main window class name

// Forward declarations of functions included in this code module:
ATOM				MyRegisterClass(HINSTANCE hInstance);
BOOL				InitInstance(HINSTANCE, int);
LRESULT CALLBACK	WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK	About(HWND, UINT, WPARAM, LPARAM);


typedef struct { BYTE* ptr; int len; LONG width; LONG height; } Bitmap;

// this is really sad, i have to do it manaully
HBITMAP CreateGrayscaleDIB(Bitmap* bits)
{
	struct { BITMAPINFOHEADER bmiHeader; RGBQUAD bmiColors[256]; } bmi;

	bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
	bmi.bmiHeader.biWidth = bits->width;
	bmi.bmiHeader.biHeight = -bits->height;  // bitmap will be "top-down"
	//bmi.bmiHeader.biHeight = bits->height;  // bitmap will be "bottom-up"
	bmi.bmiHeader.biPlanes = 1;
	bmi.bmiHeader.biBitCount = 8;
	bmi.bmiHeader.biCompression = BI_RGB;
	bmi.bmiHeader.biSizeImage = 0;
	bmi.bmiHeader.biXPelsPerMeter = 0;
	bmi.bmiHeader.biYPelsPerMeter = 0;
	bmi.bmiHeader.biClrUsed = 0;//256;
	bmi.bmiHeader.biClrImportant = 0;//256;

	// set grayscale color map
	memset(bmi.bmiColors, 0, sizeof(bmi.bmiColors));
	for (int i = 0; i < 256; i++)
	{
		bmi.bmiColors[ i ].rgbRed = i;
		bmi.bmiColors[ i ].rgbGreen = i;
		bmi.bmiColors[ i ].rgbBlue = i;
	}

	HBITMAP hbitmap = ::CreateDIBSection(NULL, (BITMAPINFO*)&bmi, DIB_RGB_COLORS, (void**)(&bits->ptr), NULL, 0);
	assert (hbitmap);
	bits->len = bits->width * bits->height;
	return hbitmap;
}


// freetype drawing code

#include <ft2build.h>
#include FT_FREETYPE_H

FT_Face g_font_face;
struct { char* ptr; size_t len; } g_text;
HDC g_memdc = NULL;
HGDIOBJ g_prevobj = NULL;
HBITMAP g_hbitmap = NULL;
Bitmap g_bitmap;
const int FONTSIZE = 24;

int OnCreate(HWND hWnd)
{
	FT_Error error;
	g_text.ptr = "#FreeType 2 library test.";
	g_text.len = strlen(g_text.ptr);

	// initialize freetype library
	FT_Library library;
	error = FT_Init_FreeType(&library);
	if (error) return -1;

	// load a typeface
	char font_path[1024];
	::ExpandEnvironmentStringsA("%SystemRoot%/fonts/arial.ttf", font_path, 1024-1);
	error = FT_New_Face(library, font_path, 0, &g_font_face);
	if (error) return -1;

	// get current DPI
	DEVMODE dev_mode;
	dev_mode.dmSize = sizeof (DEVMODE);
	::EnumDisplaySettingsEx(NULL, ENUM_CURRENT_SETTINGS, &dev_mode, 0);
	WORD& dpi = dev_mode.dmLogPixels;

	// set font size in points, using current DPI
	error = FT_Set_Char_Size(g_font_face, FONTSIZE*64,0, dpi,0);
	if (error) return -1;

	g_memdc = ::CreateCompatibleDC(GetDC(hWnd));
	g_bitmap.height = g_font_face->max_advance_height;
	g_bitmap.width = g_font_face->max_advance_width;
	g_hbitmap = CreateGrayscaleDIB(&g_bitmap);
	g_prevobj = ::SelectObject(g_memdc, g_hbitmap);
	assert (g_prevobj && HGDI_ERROR != g_prevobj);
	return 0;
}


void OnDestroy()
{
	::SelectObject(g_memdc, g_prevobj);
	::DeleteObject(g_hbitmap);
	::DeleteDC(g_memdc);
}


void OnDrawWindow(HDC hdc)
{
	FT_Error error;
	int pen_x = 0;
	for (unsigned int i = 0; i < g_text.len; i++)
	{
		FT_UInt glyph_index = FT_Get_Char_Index(g_font_face, g_text.ptr[i]); 
		assert (glyph_index);
		error = FT_Load_Glyph(g_font_face,     // handle to face object
		                      glyph_index,     // glyph index
		                      FT_LOAD_RENDER); // load flags
		assert (!error);
		//error = FT_Render_Glyph(g_font_face->glyph,     // glyph slot
		//                        FT_RENDER_MODE_NORMAL); // render mode
		//assert (!error);

		int& glyph_pitch     = g_font_face->glyph->bitmap.pitch;
		int& glyph_height    = g_font_face->glyph->bitmap.rows;
		int& glyph_width     = g_font_face->glyph->bitmap.width;
		int& glyph_bearing_x = g_font_face->glyph->bitmap_left;
		int& glyph_bearing_y = g_font_face->glyph->bitmap_top;
		int  glyph_advance   = g_font_face->glyph->advance.x / 64;
		int  hori_advance    = g_font_face->glyph->metrics.horiAdvance / 64;
		int  vert_advance    = g_font_face->glyph->metrics.vertAdvance / 64;
		int face_ascender  = g_font_face->ascender  / 64;
		int face_descender = g_font_face->descender / 64;
		int face_height    = g_font_face->height    / 64;

		memset(g_bitmap.ptr, 160, g_bitmap.len);
		for (int y = 0; y < glyph_height; y++)
		{
			int src_row_start = y * glyph_pitch;
			int dst_row_start = (y + (vert_advance - glyph_bearing_y)) * g_bitmap.width;
			memcpy(g_bitmap.ptr + dst_row_start + glyph_bearing_x,
			       g_font_face->glyph->bitmap.buffer + src_row_start,
			       glyph_pitch);
		}
		::BitBlt(hdc, pen_x, 0, glyph_advance, face_height, g_memdc, 0, 0, SRCCOPY);
		pen_x += glyph_advance;
	}
}



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
	LoadString(hInstance, IDS_APP_TITLE, g_title, MAX_LOADSTRING);
	LoadString(hInstance, IDC_EXAMPLE1, g_window_class, MAX_LOADSTRING);
	MyRegisterClass(hInstance);

	// Perform application initialization:
	if (!InitInstance (hInstance, nCmdShow))
	{
		return FALSE;
	}

	hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_EXAMPLE1));

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



//
//  FUNCTION: MyRegisterClass()
//
//  PURPOSE: Registers the window class.
//
//  COMMENTS:
//
//    This function and its usage are only necessary if you want this code
//    to be compatible with Win32 systems prior to the 'RegisterClassEx'
//    function that was added to Windows 95. It is important to call this function
//    so that the application will get 'well formed' small icons associated
//    with it.
//
ATOM MyRegisterClass(HINSTANCE hInstance)
{
	WNDCLASSEX wcex;

	wcex.cbSize = sizeof(WNDCLASSEX);

	wcex.style			= CS_HREDRAW | CS_VREDRAW;
	wcex.lpfnWndProc	= WndProc;
	wcex.cbClsExtra		= 0;
	wcex.cbWndExtra		= 0;
	wcex.hInstance		= hInstance;
	wcex.hIcon			= LoadIcon(hInstance, MAKEINTRESOURCE(IDI_EXAMPLE1));
	wcex.hCursor		= LoadCursor(NULL, IDC_ARROW);
	wcex.hbrBackground	= (HBRUSH)(COLOR_WINDOW+1);
	wcex.lpszMenuName	= MAKEINTRESOURCE(IDC_EXAMPLE1);
	wcex.lpszClassName	= g_window_class;
	wcex.hIconSm		= LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

	return RegisterClassEx(&wcex);
}

//
//   FUNCTION: InitInstance(HINSTANCE, int)
//
//   PURPOSE: Saves instance handle and creates main window
//
//   COMMENTS:
//
//        In this function, we save the instance handle in a global variable and
//        create and display the main program window.
//
BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
   HWND hWnd;

   g_hinst = hInstance; // Store instance handle in our global variable

   hWnd = CreateWindow(g_window_class, g_title, WS_OVERLAPPEDWINDOW,
      CW_USEDEFAULT, 0, CW_USEDEFAULT, 0, NULL, NULL, hInstance, NULL);

   if (!hWnd)
   {
      return FALSE;
   }

   ShowWindow(hWnd, nCmdShow);
   UpdateWindow(hWnd);

   return TRUE;
}

//
//  FUNCTION: WndProc(HWND, UINT, WPARAM, LPARAM)
//
//  PURPOSE:  Processes messages for the main window.
//
//  WM_COMMAND	- process the application menu
//  WM_PAINT	- Paint the main window
//  WM_DESTROY	- post a quit message and return
//
//
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	int wmId, wmEvent;
	PAINTSTRUCT ps;
	HDC hdc;

	switch (message)
	{
	case WM_COMMAND:
		wmId    = LOWORD(wParam);
		wmEvent = HIWORD(wParam);
		// Parse the menu selections:
		switch (wmId)
		{
		case IDM_ABOUT:
			DialogBox(g_hinst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
			break;
		case IDM_EXIT:
			DestroyWindow(hWnd);
			break;
		default:
			return DefWindowProc(hWnd, message, wParam, lParam);
		}
		break;
	case WM_PAINT:
		hdc = BeginPaint(hWnd, &ps);
		// TODO: Add any drawing code here...
		OnDrawWindow(hdc);
		EndPaint(hWnd, &ps);
		break;
	case WM_CREATE:
		return OnCreate(hWnd);
	case WM_DESTROY:
		OnDestroy();
		PostQuitMessage(0);
		break;
	default:
		return DefWindowProc(hWnd, message, wParam, lParam);
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
