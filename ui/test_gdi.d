pragma(lib, "win32.lib");
static import win32 = win32.windows;

string szTitle = "test";  // The title bar text
string szWindowClass = "test_window";  // the main window class name

void main()
{
	win32.HMODULE hInstance = win32.GetModuleHandle(null);
	// init instance
	win32.WNDCLASSEX wcex;
	wcex.style			= win32.CS_HREDRAW | win32.CS_VREDRAW;
	wcex.lpfnWndProc	= &WndProc;
	wcex.hInstance		= hInstance;
	wcex.hbrBackground	= cast(win32.HBRUSH)(win32.COLOR_WINDOW+1);
	wcex.lpszClassName	= szWindowClass.ptr;
	win32.RegisterClassEx(&wcex);
	win32.HWND hWnd = win32.CreateWindow(szWindowClass.ptr, szTitle.ptr, win32.WS_OVERLAPPEDWINDOW,
				win32.CW_USEDEFAULT, 0, win32.CW_USEDEFAULT, 0, null, null, hInstance, null);
	if (!hWnd)
		throw new Exception("CreateWindow failed");

	win32.ShowWindow(hWnd, win32.SW_SHOWNORMAL);
	win32.UpdateWindow(hWnd);

	// Main message loop:
	win32.MSG msg;
	while (win32.GetMessage(&msg, null, 0, 0))
	{
		win32.DispatchMessage(&msg);
	}
}


extern (Windows)
win32.LRESULT WndProc(win32.HWND hWnd, win32.UINT message, win32.WPARAM wParam, win32.LPARAM lParam)
{
	switch (message)
	{
	case win32.WM_PAINT:
		win32.PAINTSTRUCT ps;
		win32.HDC hdc = win32.BeginPaint(hWnd, &ps);
		// TODO: Add any drawing code here...
		win32.EndPaint(hWnd, &ps);
		break;
	case win32.WM_DESTROY:
		win32.PostQuitMessage(0);
		break;
	default:
		return win32.DefWindowProc(hWnd, message, wParam, lParam);
	}
	return 0;
}
