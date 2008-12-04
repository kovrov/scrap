pragma(lib, "win32.lib");
static import win32 = win32.windows;


void main()
{
	// init instance
	win32.WNDCLASSEX wcex;
	wcex.style			= win32.CS_HREDRAW | win32.CS_VREDRAW;
	wcex.lpfnWndProc	= &WndProc;
	wcex.hInstance		= win32.GetModuleHandle(null);
	wcex.hbrBackground	= cast(win32.HBRUSH)(win32.COLOR_WINDOW+1);
	wcex.lpszClassName	= "test_window";
	if (!win32.RegisterClassEx(&wcex))
		throw new Exception("RegisterClass failed");
	win32.HWND hWnd = win32.CreateWindow(wcex.lpszClassName, "test",
				win32.WS_OVERLAPPEDWINDOW, win32.CW_USEDEFAULT,
				0, win32.CW_USEDEFAULT, 0, null, null, wcex.hInstance, null);
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
	case win32.WM_PAINT:  // http://msdn.microsoft.com/library/ms534901
		win32.PAINTSTRUCT ps;
		win32.HDC hdc = win32.BeginPaint(hWnd, &ps);
		// ...
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
