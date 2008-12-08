pragma(lib, "win32.lib");
static import win32 = win32.windows;
import std.string;
import event;

class Window
{
	event.Manager event_mgr;
	private win32.HWND handle;
	private static typeof(this)[win32.HWND] _windows;
	private static invariant(char*) _classnamez = "test_window";
	private static extern (Windows)
	win32.LRESULT WndProc(win32.HWND hWnd, win32.UINT message, win32.WPARAM wParam, win32.LPARAM lParam)
	{
		switch (message)
		{
		case win32.WM_PAINT:  // http://msdn.microsoft.com/library/ms534901
			auto paint = _windows[hWnd].paint_handler;
			if (paint !is null)
			{
				win32.PAINTSTRUCT ps;
				win32.HDC hdc = win32.BeginPaint(hWnd, &ps);
				// http://msdn.microsoft.com/en-us/library/ms969905.aspx
				win32.HDC buffer_dc = win32.CreateCompatibleDC(hdc);
				win32.HBITMAP bitmap = win32.CreateCompatibleBitmap(hdc, ps.rcPaint.right, ps.rcPaint.bottom);
				win32.HBITMAP old_bitmap = win32.SelectObject(buffer_dc, bitmap);
				paint(buffer_dc);
				win32.BitBlt(hdc, 0, 0, ps.rcPaint.right, ps.rcPaint.bottom, buffer_dc, 0, 0, win32.SRCCOPY);
				win32.SelectObject(buffer_dc, old_bitmap);
				win32.DeleteObject(bitmap);
				win32.DeleteDC(buffer_dc);
				win32.EndPaint(hWnd, &ps);
			}
			break;
		case win32.WM_MOUSEMOVE:  // http://msdn.microsoft.com/library/ms645616
			_windows[hWnd].event_mgr.dispatch(
				event.MouseEvent(event.MOUSE.MOVE, Point(win32.LOWORD(lParam), win32.HIWORD(lParam))));
			break;
		case win32.WM_DESTROY:
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
		wcex.style			= win32.CS_HREDRAW | win32.CS_VREDRAW;
		wcex.lpfnWndProc	= &WndProc;
		wcex.hInstance		= win32.GetModuleHandle(null);
		wcex.hCursor        = win32.LoadCursor(null,  win32.IDC_ARROW);
		wcex.lpszClassName	= _classnamez;
		if (!win32.RegisterClassEx(&wcex))
			throw new Exception("RegisterClass failed");
	}


	enum STYLE
	{
		DEFAULT,
		BORDERLESS,
		DIALOG,
		TOOL
	}
	struct Settings
	{
		string title;
		bool visible = true;
		int width = win32.CW_USEDEFAULT;
		int height = 0;
		bool resizable = false;
		bool fullscreen = false;
		bool vsync = true;
		STYLE style;
		//display=null;
		//screen=null;
		//config=null;
		//context=null;
	}

	this()
	{
		this(Settings());
	}
	this(ref Settings settings)
	{
		event_mgr = new event.Manager;
		win32.DWORD style = win32.WS_OVERLAPPEDWINDOW;
		if (settings.width > 0 && settings.height > 0)
		{
			win32.RECT rect = win32.RECT(0,0, settings.width, settings.height);
			assert (win32.AdjustWindowRect(&rect, style, win32.FALSE));
			settings.width = rect.right - rect.left;
			settings.height = rect.bottom - rect.top;
		}
		else
		{
			settings.width = win32.CW_USEDEFAULT;
			settings.height = 0; // ignored
		}
		handle = win32.CreateWindow(_classnamez, toStringz(settings.title),
					style,
					win32.CW_USEDEFAULT, 0,
					settings.width, settings.height,
					null, null, win32.GetModuleHandle(null), null);
		if (!handle)
			throw new Exception("CreateWindow failed");
		_windows[handle] = this;
		_windows.rehash;
		if (settings.visible)
			this.visible(true);
	}
	void visible(bool show)
	{
		win32.ShowWindow(handle, show?win32.SW_SHOWNORMAL:win32.SW_HIDE);
		win32.UpdateWindow(handle);
	}
	void redraw()
	{
		win32.InvalidateRect(this.handle, null, false);
	}
	void delegate(win32.HDC hdc) paint_handler;
}
