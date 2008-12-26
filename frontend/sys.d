pragma(lib, "win32.lib");
static import win32 = win32.windows;

import std.string;

static import generic;
alias generic.Point!(short) Point;
alias generic.Size!(ushort) Size;


int messageLoop()
{
	win32.MSG msg;
	while (win32.GetMessage(&msg, null, 0, 0))
	{
		win32.DispatchMessage(&msg);
	}
	return 0;
}

interface Window
{
	enum STYLE
	{
		DEFAULT,
		BORDERLESS,
		DIALOG,
		TOOL
	}
	enum FLAG
	{
		hidden     = 1,
		resizable  = 1<<1,
		fullscreen = 1<<2,
		vsync      = 1<<3
	}
	/* Factory method */

	abstract void visible(bool);
	abstract void redraw();
}

enum MOUSE
{
	LEFT_DBLCLK,
	LEFT_DOWN,
	LEFT_UP,
	MIDDLE_DBLCLK,
	MIDDLE_DOWN,
	MIDDLE_UP,
	RIGTH_DBLCLK,
	RIGTH_DOWN,
	RIGTH_UP,
	MOVE,
}

class WindowGDI(IOMANAGER) : Window
{
	IOMANAGER io;
	private win32.HWND handle;
	private static typeof(this)[win32.HWND] _windows;
	private static invariant(char*) _classnamez = "test_window";

	private static extern (Windows)
	win32.LRESULT WndProc(win32.HWND hWnd, win32.UINT message, win32.WPARAM wParam, win32.LPARAM lParam)
	{
		switch (message)
		{
		case win32.WM_PAINT:  // http://msdn.microsoft.com/library/ms534901
			_windows[hWnd].io.on_paint(hWnd);
			break;
		// The left mouse button
		case win32.WM_LBUTTONDBLCLK: // double-clicked http://msdn.microsoft.com/library/ms645606
		case win32.WM_LBUTTONDOWN:   // pressed.
		case win32.WM_LBUTTONUP:     // released.
		// The middle mouse button
		case win32.WM_MBUTTONDBLCLK: // double-clicked.
		case win32.WM_MBUTTONDOWN:   // pressed.
		case win32.WM_MBUTTONUP:     // released.
		// The right mouse button
		case win32.WM_RBUTTONDBLCLK: // double-clicked.
		case win32.WM_RBUTTONDOWN:   // pressed.
		case win32.WM_RBUTTONUP:     // released.
		// Windows 2000/Windows XP: An X mouse button
		//case win32.WM_XBUTTONDBLCLK: // double-clicked.
		//case win32.WM_XBUTTONDOWN:   // pressed.
		//case win32.WM_XBUTTONUP:     // released.
		break;
		// Mouse cursor has moved (if not captured, within the client area)
		case win32.WM_MOUSEMOVE:  // http://msdn.microsoft.com/library/ms645616
/*	MOUSE.LEFT_DBLCLK
	MOUSE.LEFT_DOWN
	MOUSE.LEFT_UP
	MOUSE.MIDDLE_DBLCLK
	MOUSE.MIDDLE_DOWN
	MOUSE.MIDDLE_UP
	MOUSE.RIGTH_DBLCLK
	MOUSE.RIGTH_DOWN
	MOUSE.RIGTH_UP
*/
			_windows[hWnd].io.dispatch_mouse_input(Point(win32.LOWORD(lParam), win32.HIWORD(lParam)), MOUSE.MOVE);
			break;
		case win32.WM_MOUSELEAVE:  // http://msdn.microsoft.com/library/ms645615
			assert (false);  // temp
			break;
		case win32.WM_DESTROY:
			_windows.remove(hWnd);
			if (_windows.length > 0)
				_windows.rehash;
			else
				win32.PostQuitMessage(0);
			break;
		default:
			return win32.DefWindowProc(hWnd, message, wParam, lParam);
		}
		return 0;
	}

	static this()
	{
		win32.WNDCLASSEX wcex;
		wcex.style			= win32.CS_HREDRAW | win32.CS_VREDRAW; // CS_DBLCLKS
		wcex.lpfnWndProc	= &WndProc;
		wcex.hInstance      = win32.GetModuleHandle(null);
		wcex.hCursor		= win32.LoadCursor(null, win32.IDC_ARROW);
		wcex.lpszClassName	= _classnamez;
		if (!win32.RegisterClassEx(&wcex))
			throw new Exception("RegisterClass failed");
	}

	/* Factory method */
	static typeof(this) opCall(TUPLE...)(TUPLE tuple)
	{
		//display=null;
		//screen=null;
		//config=null;
		//context=null;
		string title = "default";
		bool fullscreen, vsync, hidden;
		win32.DWORD style = win32.WS_OVERLAPPEDWINDOW, style_ex = 0;
		win32.RECT size_rect = win32.RECT(0,0, win32.CW_USEDEFAULT, 0);
		foreach (e; tuple)
		{
			static if (typeid(typeof(e)) is typeid(FLAG))
			{
				if (!(e&FLAG.resizable))
					style ^= (win32.WS_THICKFRAME | win32.WS_MAXIMIZEBOX);
				fullscreen = cast(bool)(e&FLAG.fullscreen);
				vsync      = cast(bool)(e&FLAG.vsync);
				hidden     = cast(bool)(e&FLAG.hidden);
			}
			static if (typeid(typeof(e)) is typeid(Size))
			{
				size_rect.right = e.width;
				size_rect.bottom = e.height;
			}
			static if (typeid(typeof(e)) is typeid(string))
			{
				title = e;
			}
		}

		if (size_rect.right > 0 && size_rect.bottom > 0)
		{
			win32.AdjustWindowRectEx(&size_rect, style, win32.FALSE, style_ex);
		}

		win32.HWND hwnd = win32.CreateWindowEx(style_ex,
					_classnamez, toStringz(title), style,
					win32.CW_USEDEFAULT, 0,
					size_rect.right - size_rect.left, size_rect.bottom - size_rect.top,
					null, null, win32.GetModuleHandle(null), null);
		if (!hwnd)
			throw new Exception("CreateWindow failed");

		auto window = new typeof(this);
		window.io = new IOMANAGER(window);
		window.handle = hwnd;
		_windows[hwnd] = window;
		_windows.rehash;
		if (!hidden)
			window.visible(true);
		return window;
	}

	override void visible(bool show)
	{
		win32.ShowWindow(handle, show?win32.SW_SHOWNORMAL:win32.SW_HIDE);
		win32.UpdateWindow(handle);
	}

	override void redraw()
	{
		win32.InvalidateRect(this.handle, null, false);
	}
}
