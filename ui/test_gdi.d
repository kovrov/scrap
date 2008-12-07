pragma(lib, "win32.lib");
static import win32 = win32.windows;
import std.string;
static import generic;
alias generic.Point!(short) Point;
alias generic.Size!(ushort) Size;
alias generic.Rect!(short, ushort) Rect;

class SysWindow
{
	event.Manager event_mgr;
	private win32.HWND handle;
	private static SysWindow[win32.HWND] _windows;
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

import std.stdio;
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


class Window : event.TargetNode
{
	this(string name, event.TargetNode parent) { super(name, parent); }
}

class Group : event.TargetNode
{
	this(string name, event.TargetNode parent) { super(name, parent); }
}

class Radio : event.TargetNode
{
	this(string name, event.TargetNode parent) { super(name, parent); }
}

class Button : event.TargetNode
{
	this(string name, event.TargetNode parent) { super(name, parent); }
}

class Label : event.TargetNode
{
	this(string name, event.TargetNode parent) { super(name, parent); }
}

class Dialog : event.TargetNode
{
	this(string name, event.TargetNode parent) { super(name, parent); }
}

event.TargetNode genTestData()
{
	auto root = new event.TargetNode("root");
	root.rect.size = Size(640,480);
	  auto dlg = new Dialog("dlg", root);
	  dlg.rect = Rect(Point(200,200),Size(400,200));  // [200,200-600,400]
	    auto b2 = new Button("b2", dlg);
	    b2.rect = Rect(Point(10,10),Size(48,18));     // [210,210-228,258]
	    auto b3 = new Button("b3", dlg);
	    b3.rect = Rect(Point(10,40),Size(50,20));     // [210,240-230,290]
	    auto l2 = new Label("l2", dlg);
	    l2.rect = Rect(Point(10,70),Size(50,20));     // [210,270-230,320]
	  auto wnd = new Window("wnd", root);
	  wnd.rect = Rect(Point(100,100),Size(400,200));  // [100,100-500,300]
	    auto b1 = new Button("b1", wnd);
	    b1.rect = Rect(Point(10,170),Size(30,20));    // [110,270-130,300]
	    auto l1 = new Label("l1", wnd);
	    l1.rect = Rect(Point(50,170),Size(30,20));    // [150,440-170,470]
	    auto grp = new Group("grp", wnd);
	    grp.rect = Rect(Point(10,10),Size(290,150));  // [110,110-400,260]
	      auto r1 = new Radio("r1", grp);
	      r1.rect = Rect(Point(10,10),Size(30,10));   // [120,120-130,170]
	      auto r2 = new Radio("r2", grp);
	      r2.rect = Rect(Point(10,30),Size(30,10));   // [120,140-130,190]
	return root;
}


static import event;
void main()
{
	event.TargetNode tracked;
	event.TargetNode root = genTestData();

	SysWindow.Settings settings;
	settings.title = "test";
	settings.visible = false;
	settings.width = 640;
	settings.height = 480;
	auto window = new SysWindow(settings);

	window.event_mgr.register(
		delegate (ref event.MouseEvent ev)
		{
			auto target = event.findControl(root, ev.pos);
			if (tracked !is target)
			{
				tracked = target;
				window.redraw();
			}
		});
	window.paint_handler = delegate(win32.HDC hdc)
	{
		auto original = win32.GetCurrentObject(hdc, win32.OBJ_BRUSH);
		foreach_reverse(ref node; root)
		{
			if (node is tracked)
				win32.SelectObject(hdc, win32.GetStockObject(win32.GRAY_BRUSH));

			Point pos = node.position_abs();
			win32.Rectangle(hdc,
					pos.x, pos.y,
					pos.x+node.rect.size.width, pos.y+node.rect.size.height);

			if (node is tracked)
				win32.SelectObject(hdc, original);
		}
	};
	window.visible(true);

	// Main message loop:
	win32.MSG msg;
	while (win32.GetMessage(&msg, null, 0, 0))
	{
		win32.DispatchMessage(&msg);
	}
}
