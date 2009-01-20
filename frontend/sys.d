/*
  TODO:
   * add opengl window
   * refactor windows heirarchy
   * mouse/keyboard state?
*/
import std.stdio;

pragma(lib, "win32.lib");
static import win32 = win32.windows;

import std.string;

static import generic;
alias generic.Point!(short) Point;
alias generic.Size!(ushort) Size;


void quit()
{
	win32.PostQuitMessage(0);
}

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
	abstract void visible(bool);
	abstract void redraw();
}

enum MOUSE
{
	PRESS,
	RELEASE,
	MOVE,
}

enum KEY
{
	PRESS,
	RELEASE,
}

bool[256] keyboardState; // virtual key codes


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

		case win32.WM_INPUT:  // http://msdn.microsoft.com/library/ms645590
			byte[64] buffer;
			uint buffer_size = buffer.length;
			assert (win32.GetRawInputData(cast(win32.HRAWINPUT)lParam, win32.RID_INPUT,
			                              buffer.ptr, &buffer_size,
			                              win32.RAWINPUTHEADER.sizeof) != -1);
			auto raw = cast(win32.RAWINPUT*)buffer.ptr;
			if (raw.header.dwType == win32.RIM_TYPEKEYBOARD)
			{
				if (raw.data.keyboard.VKey > 0x00 && raw.data.keyboard.VKey < 0xFF)
				{
					switch (raw.data.keyboard.Message)
					{
					case win32.WM_KEYDOWN, win32.WM_SYSKEYDOWN:
						keyboardState[raw.data.keyboard.VKey] = true;
						_windows[hWnd].io.dispatch_KEYBOARD_input(wParam, KEY.PRESS);
						break;
					case win32.WM_KEYUP, win32.WM_SYSKEYUP:
						keyboardState[raw.data.keyboard.VKey] = false;
						_windows[hWnd].io.dispatch_KEYBOARD_input(wParam, KEY.RELEASE);
						break;
					}
				}
			}
			else if (raw.header.dwType == win32.RIM_TYPEMOUSE)
			{
				writefln("Mouse: usFlags=%04x ulButtons=%04x usButtonFlags=%04x usButtonData=%04x ulRawButtons=%04x lLastX=%04x lLastY=%04x ulExtraInformation=%04x",
					raw.data.mouse.usFlags,
					raw.data.mouse.ulButtons,
					raw.data.mouse.usButtonFlags,
					raw.data.mouse.usButtonData,
					raw.data.mouse.ulRawButtons,
					raw.data.mouse.lLastX,
					raw.data.mouse.lLastY,
					raw.data.mouse.ulExtraInformation);
			}
			// must call so the system can perform the cleanup
			return win32.DefWindowProc(hWnd, message, wParam, lParam);

		// mouse input
		case win32.WM_LBUTTONDBLCLK, win32.WM_RBUTTONDBLCLK, win32.WM_MBUTTONDBLCLK:
			assert (false);  // break;
		case win32.WM_LBUTTONDOWN, win32.WM_LBUTTONUP:    // left mouse button
		case win32.WM_RBUTTONDOWN, win32.WM_RBUTTONUP:    // right mouse button
		case win32.WM_MBUTTONDOWN, win32.WM_MBUTTONUP:    // middle mouse button
			int button =
					message == win32.WM_LBUTTONDOWN || message == win32.WM_LBUTTONUP ? 0:
					message == win32.WM_RBUTTONDOWN || message == win32.WM_RBUTTONUP ? 1:
					message == win32.WM_MBUTTONDOWN || message == win32.WM_MBUTTONUP ? 2:
					-1;  // error
			MOUSE type = message == win32.WM_LBUTTONUP ||
			             message == win32.WM_RBUTTONUP ||
			             message == win32.WM_MBUTTONUP ? MOUSE.RELEASE : MOUSE.PRESS;
			_windows[hWnd].io.dispatch_MOUSE_input(Point(win32.LOWORD(lParam), win32.HIWORD(lParam)), type, button);
			break;
		// Windows 2000/Windows XP: An X mouse button
		//case win32.WM_XBUTTONDBLCLK, win32.WM_XBUTTONDOWN, win32.WM_XBUTTONUP:
		//	break;
		// Mouse cursor has moved (if not captured, within the client area)
		case win32.WM_MOUSEMOVE:  // http://msdn.microsoft.com/library/ms645616
			_windows[hWnd].io.dispatch_MOUSE_input(Point(win32.LOWORD(lParam), win32.HIWORD(lParam)), MOUSE.MOVE);
			break;
		case win32.WM_MOUSELEAVE:  // http://msdn.microsoft.com/library/ms645615
			assert (false);  // break;

		case win32.WM_KEYDOWN, win32.WM_KEYUP, win32.WM_SYSKEYDOWN, win32.WM_SYSKEYUP:
			auto action = (message == win32.WM_KEYDOWN || message == win32.WM_SYSKEYDOWN) ? KEY.PRESS : KEY.RELEASE;
			keyboardState[wParam] = (action == KEY.PRESS);
			if (_windows[hWnd].io.dispatch_KEYBOARD_input(wParam, action))
				break;
			return win32.DefWindowProc(hWnd, message, wParam, lParam);

		case win32.WM_GETMINMAXINFO:
			auto mmi = cast(win32.MINMAXINFO*)lParam;
			Size size;
			auto w = hWnd in _windows;
			if (w !is null && w.io.query_MINMAX_info(&size))
			{
				mmi.ptMinTrackSize.x = size.width + win32.GetSystemMetrics(win32.SM_CXFRAME)*2;
				mmi.ptMinTrackSize.y = size.height + win32.GetSystemMetrics(win32.SM_CYFRAME)*2 + win32.GetSystemMetrics(win32.SM_CYCAPTION);
			}
			break;

		case win32.WM_NCCALCSIZE:  // http://msdn.microsoft.com/ms632634
			auto ret = win32.DefWindowProc(hWnd, message, wParam, lParam);
			if (wParam != win32.TRUE)  // first time
			{
				auto r = cast(win32.RECT*)lParam;
			}
			else
			{
				// http://blogs.msdn.com/oldnewthing/archive/2003/09/15/54925.aspx
				auto nccp = cast(win32.NCCALCSIZE_PARAMS*)lParam;
				const win32.RECT in_newWindowRect = nccp.rgrc[0];
				const win32.RECT in_oldWindowRect = nccp.rgrc[1];
				const win32.RECT in_oldClientRect = nccp.rgrc[2];
				const win32.RECT* out_newClientRect = &nccp.rgrc[0];
				//const win32.RECT* out_validDstRect = &nccp.rgrc[1];
				//const win32.RECT* out_validSrcRect = &nccp.rgrc[2];
			}
			return ret;

		case win32.WM_SIZE:  // http://msdn.microsoft.com/library/ms632646
			writefln("WM_SIZE:%s:%d,%d",
						wParam == win32.SIZE_MAXHIDE ? "MAXHIDE" :
						wParam == win32.SIZE_MAXIMIZED ? "MAXIMIZED" :
						wParam == win32.SIZE_MAXSHOW ?   "MAXSHOW" :
						wParam == win32.SIZE_MINIMIZED ? "MINIMIZED" :
						wParam == win32.SIZE_RESTORED ?  "RESTORED" :
						null,
					win32.LOWORD(lParam), win32.HIWORD(lParam));

			switch (wParam)
			{
			case win32.SIZE_RESTORED, win32.SIZE_MAXIMIZED:
				_windows[hWnd].io.notify_SIZE_state_change(win32.LOWORD(lParam), win32.HIWORD(lParam), wParam == win32.SIZE_MAXIMIZED);
				break;
			case win32.SIZE_MINIMIZED:
				break;
			//case win32.SIZE_MAXSHOW, win32.SIZE_MAXHIDE:
			}
			break;

		case win32.WM_DESTROY:
			auto self = _windows[hWnd];
			_windows.remove(hWnd);
			if (_windows.length > 0)
				_windows.rehash;
			else
				win32.PostQuitMessage(0);
			delete self;
			break;
		case win32.WM_CLOSE:
			if (_windows[hWnd].io.confirm_CLOSE_action())
				return win32.DefWindowProc(hWnd, message, wParam, lParam);
			break;
		// generic asserts
		case win32.WM_ENABLE: assert (false, "top-level windows should not be disabled/enabled");
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

		/+
		// raw input
		enum HID_USAGE_PAGE { GENERIC = 0x01 }
		enum HID_USAGE { GENERIC_MOUSE = 0x02, GENERIC_KEYBOARD = 0x06 }

		win32.RAWINPUTDEVICE Rid[1];

		Rid[0].usUsagePage = HID_USAGE_PAGE.GENERIC;
		Rid[0].usUsage = HID_USAGE.GENERIC_KEYBOARD;
		Rid[0].dwFlags = win32.RIDEV_NOHOTKEYS | // no logo/super key
						win32.RIDEV_NOLEGACY; // no WM_KEYDOWN/WM_KEYUP, WM_SYSKEYDOWN/WM_SYSKEYUP ...
							
		Rid[0].hwndTarget = null;

		//Rid[0].usUsagePage = HID_USAGE_PAGE.GENERIC;
		//Rid[0].usUsage = HID_USAGE.GENERIC_MOUSE;
		//Rid[0].dwFlags = win32.RIDEV_NOLEGACY;   // adds HID mouse and also ignores legacy mouse messages
		//Rid[0].hwndTarget = null;

		if (win32.RegisterRawInputDevices(Rid.ptr, Rid.length, win32.RAWINPUTDEVICE.sizeof) == win32.FALSE)
			writeln("registration failed");  // Call GetLastError for the cause of the error
		+/
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

		// temp hack to be able to output to console
		win32.AttachConsole(win32.ATTACH_PARENT_PROCESS);

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

// win32 virtual key codes
// http://msdn.microsoft.com/library/ms645540
invariant (string[256]) keys = [
	          	null,
	/* 0x01 */	"Left mouse",
	/* 0x02 */	"Right mouse",
	/* 0x03 */	"Break",
	/* 0x04 */	"Middle mouse",
	/* 0x05 */	"XBUTTON1",
	/* 0x06 */	"XBUTTON2",
	/* 0x07 */	null,  // undefined
	/* 0x08 */	"Backspace",
	/* 0x09 */	"Tab",
	/* 0x0A */	null,  // reserved
	/* 0x0B */	null,  // reserved
	/* 0x0C */	"Clear",
	/* 0x0D */	"Enter",  // both, keyboard and numpad
	/* 0x0E */	null,  // undefined
	/* 0x0F */	null,  // undefined
	/* 0x10 */	"Shift",
	/* 0x11 */	"Control",
	/* 0x12 */	"Alt",
	/* 0x13 */	"Pause/Break",
	/* 0x14 */	"Caps Lock",
	/* 0x15 */	"Kana/Hangul mode",  // IME
	/* 0x16 */	null,  // undefined
	/* 0x17 */	"Junja mode",  // IME
	/* 0x18 */	"final mode",  // IME
	/* 0x19 */	"Hanja/Kanji mode",  // IME
	/* 0x1A */	null,  // undefined
	/* 0x1B */	"Esc",
	/* 0x1C */	"CONVERT",  // IME
	/* 0x1D */	"NONCONVERT",  // IME
	/* 0x1E */	"ACCEPT",  // IME
	/* 0x1F */	"mode change",  // IME
	/* 0x20 */	"Spacebar",
	/* 0x21 */	"Page Up",
	/* 0x22 */	"Page Down",
	/* 0x23 */	"End",
	/* 0x24 */	"Home",
	/* 0x25 */	"Left Arrow",
	/* 0x26 */	"Up Arrow",
	/* 0x27 */	"Right Arrow",
	/* 0x28 */	"Down Arrow",
	/* 0x29 */	"Select",
	/* 0x2A */	"Print",
	/* 0x2B */	"Execute",
	/* 0x2C */	"PrintScreen",
	/* 0x2D */	"Insert",
	/* 0x2E */	"Delete",
	/* 0x2F */	"Help",
	/* 0x30 */	"0",
	/* 0x31 */	"1",
	/* 0x32 */	"2",
	/* 0x33 */	"3",
	/* 0x34 */	"4",
	/* 0x35 */	"5",
	/* 0x36 */	"6",
	/* 0x37 */	"7",
	/* 0x38 */	"8",
	/* 0x39 */	"9",
	/* 0x3A */	null,  // Undefined
	/* 0x3B */	null,  // Undefined
	/* 0x3C */	null,  // Undefined
	/* 0x3D */	null,  // Undefined
	/* 0x3E */	null,  // Undefined
	/* 0x3F */	null,  // Undefined
	/* 0x40 */	null,  // Undefined
	/* 0x41 */	"A",
	/* 0x42 */	"B",
	/* 0x43 */	"C",
	/* 0x44 */	"D",
	/* 0x45 */	"E",
	/* 0x46 */	"F",
	/* 0x47 */	"G",
	/* 0x48 */	"H",
	/* 0x49 */	"I",
	/* 0x4A */	"J",
	/* 0x4B */	"K",
	/* 0x4C */	"L",
	/* 0x4D */	"M",
	/* 0x4E */	"N",
	/* 0x4F */	"O",
	/* 0x50 */	"P",
	/* 0x51 */	"Q",
	/* 0x52 */	"R",
	/* 0x53 */	"S",
	/* 0x54 */	"T",
	/* 0x55 */	"U",
	/* 0x56 */	"V",
	/* 0x57 */	"W",
	/* 0x58 */	"X",
	/* 0x59 */	"Y",
	/* 0x5A */	"Z",
	/* 0x5B */	"Left Windows",  // super?
	/* 0x5C */	"Right Windows",  // super?
	/* 0x5D */	"context menu", // Applications?
	/* 0x5E */	null,
	/* 0x5F */	"Sleep",  // Computer Sleep
	/* 0x60 */	"Numpad 0",
	/* 0x61 */	"Numpad 1",
	/* 0x62 */	"Numpad 2",
	/* 0x63 */	"Numpad 3",
	/* 0x64 */	"Numpad 4",
	/* 0x65 */	"Numpad 5",
	/* 0x66 */	"Numpad 6",
	/* 0x67 */	"Numpad 7",
	/* 0x68 */	"Numpad 8",
	/* 0x69 */	"Numpad 9",
	/* 0x6A */	"Multiply",
	/* 0x6B */	"Add",
	/* 0x6C */	"Separator",
	/* 0x6D */	"Subtract",
	/* 0x6E */	"Decimal",
	/* 0x6F */	"Divide",
	/* 0x70 */	"F1",
	/* 0x71 */	"F2",
	/* 0x72 */	"F3",
	/* 0x73 */	"F4",
	/* 0x74 */	"F5",
	/* 0x75 */	"F6",
	/* 0x76 */	"F7",
	/* 0x77 */	"F8",
	/* 0x78 */	"F9",
	/* 0x79 */	"F10",
	/* 0x7A */	"F11",
	/* 0x7B */	"F12",
	/* 0x7C */	"F13",
	/* 0x7D */	"F14",
	/* 0x7E */	"F15",
	/* 0x7F */	"F16",
	/* 0x80 */	"F17",
	/* 0x81 */	"F18",
	/* 0x82 */	"F19",
	/* 0x83 */	"F20",
	/* 0x84 */	"F21",
	/* 0x85 */	"F22",
	/* 0x86 */	"F23",
	/* 0x87 */	"F24",
	/* 0x88 */	null,  // unassigned
	/* 0x89 */	null,  // unassigned
	/* 0x8A */	null,  // unassigned
	/* 0x8B */	null,  // unassigned
	/* 0x8C */	null,  // unassigned
	/* 0x8D */	null,  // unassigned
	/* 0x8E */	null,  // unassigned
	/* 0x8F */	null,  // unassigned
	/* 0x90 */	"Num Lock",
	/* 0x91 */	"Scroll Lock",
	/* 0x92 */	null,  // OEM = (NEC), Dictionary (Fujitsu/OASYS)
	/* 0x93 */	null,  // OEM
	/* 0x94 */	null,  // OEM
	/* 0x95 */	null,  // OEM
	/* 0x96 */	null,  // OEM
	/* 0x97 */	null,  // unassigned
	/* 0x98 */	null,  // unassigned
	/* 0x99 */	null,  // unassigned
	/* 0x9A */	null,  // unassigned
	/* 0x9B */	null,  // unassigned
	/* 0x9C */	null,  // unassigned
	/* 0x9D */	null,  // unassigned
	/* 0x9E */	null,  // unassigned
	/* 0x9F */	null,  // unassigned
	/* 0xA0 */	"Left Shift",
	/* 0xA1 */	"Right Shift",
	/* 0xA2 */	"Left Control",
	/* 0xA3 */	"Right Control",
	/* 0xA4 */	"Left Menu",
	/* 0xA5 */	"Right Menu",
	/* 0xA6 */	"BROWSER_BACK",
	/* 0xA7 */	"BROWSER_FORWARD",
	/* 0xA8 */	"BROWSER_REFRESH",
	/* 0xA9 */	"BROWSER_STOP",
	/* 0xAA */	"BROWSER_SEARCH",
	/* 0xAB */	"BROWSER_FAVORITES",
	/* 0xAC */	"BROWSER_HOME",
	/* 0xAD */	"VOLUME_MUTE",
	/* 0xAE */	"VOLUME_DOWN",
	/* 0xAF */	"VOLUME_UP",
	/* 0xB0 */	"MEDIA_NEXT_TRACK",
	/* 0xB1 */	"MEDIA_PREV_TRACK",
	/* 0xB2 */	"MEDIA_STOP",
	/* 0xB3 */	"MEDIA_PLAY_PAUSE",
	/* 0xB4 */	"LAUNCH_MAIL",
	/* 0xB5 */	"LAUNCH_MEDIA_SELECT",
	/* 0xB6 */	"LAUNCH_APP1",
	/* 0xB7 */	"LAUNCH_APP2",
	/* 0xB8 */	null,  // reserved
	/* 0xB9 */	null,  // reserved
	/* 0xBA */	"OEM_COLON",   // ;:
	/* 0xBB */	"OEM_PLUS",    // =+
	/* 0xBC */	"OEM_COMMA",   // ,
	/* 0xBD */	"OEM_MINUS",   // -_
	/* 0xBE */	"OEM_PERIOD",  // .
	/* 0xBF */	"OEM_SLASH",   // /?
	/* 0xC0 */	"OEM_TILDE",   // `~
	/* 0xC1 */	null,  // reserved
	/* 0xC2 */	null,  // reserved
	/* 0xC3 */	null,  // reserved
	/* 0xC4 */	null,  // reserved
	/* 0xC5 */	null,  // reserved
	/* 0xC6 */	null,  // reserved
	/* 0xC7 */	null,  // reserved
	/* 0xC8 */	null,  // reserved
	/* 0xC9 */	null,  // reserved
	/* 0xCA */	null,  // reserved
	/* 0xCB */	null,  // reserved
	/* 0xCC */	null,  // reserved
	/* 0xCD */	null,  // reserved
	/* 0xCE */	null,  // reserved
	/* 0xCF */	null,  // reserved
	/* 0xD0 */	null,  // reserved
	/* 0xD1 */	null,  // reserved
	/* 0xD2 */	null,  // reserved
	/* 0xD3 */	null,  // reserved
	/* 0xD4 */	null,  // reserved
	/* 0xD5 */	null,  // reserved
	/* 0xD6 */	null,  // reserved
	/* 0xD7 */	null,  // reserved
	/* 0xD8 */	null,  // unassigned
	/* 0xD9*/	null,  // unassigned
	/* 0xDA */	null,  // unassigned
	/* 0xDB */	"OEM_LEFTBRACKET",   // [{
	/* 0xDC */	"OEM_BACKSLASH",     // \|
	/* 0xDD */	"OEM_RIGHTBRACKET",  // ]}
	/* 0xDE */	"OEM_APOSTROPHE",    // "'
	/* 0xDF */	"OEM_8",  // § !
	/* 0xE0 */	null,  // reserved
	/* 0xE1 */	null,  // OEM specific
	/* 0xE2 */	"OEM_102",  // ><
	/* 0xE3 */	null,  // OEM specific
	/* 0xE4 */	null,  // OEM specific
	/* 0xE5 */	"Process",  // IME
	/* 0xE6 */	null,  // OEM specific
	/* 0xE7 */	"PACKET",  // unicode keystrokes
	/* 0xE8 */	null,  // unassigned
	/* 0xE9 */	null,  // OEM specific (Nokia?) VK_OEM_RESET
	/* 0xEA */	null,  // OEM specific (Nokia?) VK_OEM_JUMP
	/* 0xEB */	null,  // OEM specific (Nokia?) VK_OEM_PA1
	/* 0xEC */	null,  // OEM specific (Nokia?) VK_OEM_PA2
	/* 0xED */	null,  // OEM specific (Nokia?) VK_OEM_PA3
	/* 0xEE */	null,  // OEM specific (Nokia?) VK_OEM_WSCTRL
	/* 0xEF */	null,  // OEM specific (Nokia?) VK_OEM_CUSEL
	/* 0xF0 */	null,  // OEM specific (Nokia?) VK_OEM_ATTN
	/* 0xF1 */	null,  // OEM specific (Nokia?) VK_OEM_FINNISHs
	/* 0xF2 */	null,  // OEM specific (Nokia?) VK_OEM_COPY
	/* 0xF3 */	null,  // OEM specific (Nokia?) VK_OEM_AUTOs
	/* 0xF4 */	null,  // OEM specific (Nokia?) VK_OEM_ENLW
	/* 0xF5 */	null,  // OEM specific (Nokia?) VK_OEM_BACKTAB
	/* 0xF6 */	"Attn",
	/* 0xF7 */	"CrSel",
	/* 0xF8 */	"ExSel",
	/* 0xF9 */	"Erase EOF",
	/* 0xFA */	"Play",
	/* 0xFB */	"Zoom",
	/* 0xFC */	"NONAME",  // reserved
	/* 0xFD */	"PA1",
	/* 0xFE */	"Clear",  // OEM
	          	null];
