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
	PRESS,
	RELEASE,
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
		// mouse input
		case win32.WM_LBUTTONDBLCLK:
		case win32.WM_RBUTTONDBLCLK:
		case win32.WM_MBUTTONDBLCLK:
			assert (false);  // break;
		case win32.WM_LBUTTONDOWN:  // left mouse button pressed.
		case win32.WM_LBUTTONUP:    // left mouse button released.
		case win32.WM_RBUTTONDOWN:  // right mouse button pressed.
		case win32.WM_RBUTTONUP:    // right mouse button released.
		case win32.WM_MBUTTONDOWN:  // middle mouse button pressed.
		case win32.WM_MBUTTONUP:    // middle mouse button released.
			int button = 
					message == win32.WM_LBUTTONDOWN || message == win32.WM_LBUTTONUP ? 0:
					message == win32.WM_RBUTTONDOWN || message == win32.WM_RBUTTONUP ? 1:
					message == win32.WM_MBUTTONDOWN || message == win32.WM_MBUTTONUP ? 2:
					-1;  // error
			MOUSE type = message == win32.WM_LBUTTONUP ||
			             message == win32.WM_RBUTTONUP ||
			             message == win32.WM_MBUTTONUP ? MOUSE.RELEASE : MOUSE.PRESS;
			_windows[hWnd].io.dispatch_mouse_input(Point(win32.LOWORD(lParam), win32.HIWORD(lParam)), type, button);
			break;
		// Windows 2000/Windows XP: An X mouse button
		//case win32.WM_XBUTTONDBLCLK: // double-clicked.
		//case win32.WM_XBUTTONDOWN:   // pressed.
		//case win32.WM_XBUTTONUP:     // released.
		//break;
		// Mouse cursor has moved (if not captured, within the client area)
		case win32.WM_MOUSEMOVE:  // http://msdn.microsoft.com/library/ms645616
			_windows[hWnd].io.dispatch_mouse_input(Point(win32.LOWORD(lParam), win32.HIWORD(lParam)), MOUSE.MOVE);
			break;
		case win32.WM_MOUSELEAVE:  // http://msdn.microsoft.com/library/ms645615
			assert (false);  // break;
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


invariant (string[256]) keys = [
					null,
	/*   1 0x01 */	"Left mouse",
	/*   2 0x02 */	"Right mouse",
	/*   3 0x03 */	"Break",
	/*   4 0x04 */	"Middle mouse",
	/*   5 0x05 */	"VK_XBUTTON1",
	/*   6 0x06 */	"VK_XBUTTON2",
	/*   7 0x07 */	null,
	/*   8 0x08 */	"Backspace",
	/*   9 0x09 */	"Tab",
	/*  10 0x-- */	null,
	/*  11 0x-- */	null,
	/*  12 0x0C */	"Clear",
	/*  13 0x0D */	"Enter",  // Return
	/*  14 0x-- */	null,
	/*  15 0x-- */	null,
	/*  16 0x10 */	"Shift",
	/*  17 0x11 */	"Control",
	/*  18 0x12 */	"VK_MENU",
	/*  19 0x13 */	"Pause/Break",
	/*  20 0x14 */	"Caps Lock",
	/*  21 0x15 */	"KANA/HANGEUL/HANGUL",
	/*  22 0x-- */	null,
	/*  23 0x17 */	"VK_JUNJA",
	/*  24 0x18 */	"VK_FINAL",
	/*  25 0x19 */	"HANJA/KANJI",
	/*  26 0x-- */	null,
	/*  27 0x1B */	"Esc",
	/*  28 0x1C */	"VK_CONVERT",
	/*  29 0x1D */	"VK_NONCONVERT",
	/*  30 0x1E */	"VK_ACCEPT",
	/*  31 0x1F */	"VK_MODECHANGE",
	/*  32 0x20 */	"Spacebar",
	/*  33 0x21 */	"Page Up",
	/*  34 0x22 */	"Page Down",
	/*  35 0x23 */	"End",
	/*  36 0x24 */	"Home",
	/*  37 0x25 */	"Left Arrow",
	/*  38 0x26 */	"Up Arrow",
	/*  39 0x27 */	"Right Arrow",
	/*  40 0x28 */	"Down Arrow",
	/*  41 0x29 */	"Select",
	/*  42 0x2A */	"Print",
	/*  43 0x2B */	"Execute",
	/*  44 0x2C */	"PrintScreen",
	/*  45 0x2D */	"Insert",
	/*  46 0x2E */	"Delete",
	/*  47 0x2F */	"Help",
	/*  48 0x30 */	"0",
	/*  49 0x31 */	"1",
	/*  50 0x32 */	"2",
	/*  51 0x33 */	"3",
	/*  52 0x34 */	"4",
	/*  53 0x35 */	"5",
	/*  54 0x36 */	"6",
	/*  55 0x37 */	"7",
	/*  56 0x38 */	"8",
	/*  57 0x39 */	"9",
	/*  58 0x-- */	null,
	/*  59 0x-- */	null,
	/*  60 0x-- */	null,
	/*  61 0x-- */	null,
	/*  62 0x-- */	null,
	/*  63 0x-- */	null,
	/*  64 0x-- */	null,
	/*  65 0x41 */	"A",
	/*  66 0x42 */	"B",
	/*  67 0x43 */	"C",
	/*  68 0x44 */	"D",
	/*  69 0x45 */	"E",
	/*  70 0x46 */	"F",
	/*  71 0x47 */	"G",
	/*  72 0x48 */	"H",
	/*  73 0x49 */	"I",
	/*  74 0x4A */	"J",
	/*  75 0x4B */	"K",
	/*  76 0x4C */	"L",
	/*  77 0x4D */	"M",
	/*  78 0x4E */	"N",
	/*  79 0x4F */	"O",
	/*  80 0x50 */	"P",
	/*  81 0x51 */	"Q",
	/*  82 0x52 */	"R",
	/*  83 0x53 */	"S",
	/*  84 0x54 */	"T",
	/*  85 0x55 */	"U",
	/*  86 0x56 */	"V",
	/*  87 0x57 */	"W",
	/*  88 0x58 */	"X",
	/*  89 0x59 */	"Y",
	/*  90 0x5A */	"Z",
	/*  91 0x5B */	"VK_LWIN",
	/*  92 0x5C */	"VK_RWIN",
	/*  93 0x5D */	"VK_APPS",
	/*  94 0x5E */	null,
	/*  95 0x5F */	"VK_SLEEP",
	/*  96 0x60 */	"Numpad 0",
	/*  97 0x61 */	"Numpad 1",
	/*  98 0x62 */	"Numpad 2",
	/*  99 0x63 */	"Numpad 3",
	/* 100 0x64 */	"Numpad 4",
	/* 101 0x65 */	"Numpad 5",
	/* 102 0x66 */	"Numpad 6",
	/* 103 0x67 */	"Numpad 7",
	/* 104 0x68 */	"Numpad 8",
	/* 105 0x69 */	"Numpad 9",
	/* 106 0x6A */	"Multiply",
	/* 107 0x6B */	"Add",
	/* 108 0x6C */	"Separator",
	/* 109 0x6D */	"Subtract",
	/* 110 0x6E */	"Decimal",
	/* 111 0x6F */	"Divide",
	/* 112 0x70 */	"F1",
	/* 113 0x71 */	"F2",
	/* 114 0x72 */	"F3",
	/* 115 0x73 */	"F4",
	/* 116 0x74 */	"F5",
	/* 117 0x75 */	"F6",
	/* 118 0x76 */	"F7",
	/* 119 0x77 */	"F8",
	/* 120 0x78 */	"F9",
	/* 121 0x79 */	"F10",
	/* 122 0x7A */	"F11",
	/* 123 0x7B */	"F12",
	/* 124 0x7C */	"F13",
	/* 125 0x7D */	"F14",
	/* 126 0x7E */	"F15",
	/* 127 0x7F */	"F16",
	/* 128 0x80 */	"F17",
	/* 129 0x81 */	"F18",
	/* 130 0x82 */	"F19",
	/* 131 0x83 */	"F20",
	/* 132 0x84 */	"F21",
	/* 133 0x85 */	"F22",
	/* 134 0x86 */	"F23",
	/* 135 0x87 */	"F24",
	/* 136 0x-- */	null,
	/* 137 0x-- */	null,
	/* 138 0x-- */	null,
	/* 139 0x-- */	null,
	/* 140 0x-- */	null,
	/* 141 0x-- */	null,
	/* 142 0x-- */	null,
	/* 143 0x-- */	null,
	/* 144 0x90 */	"Num Lock",
	/* 145 0x91 */	"Scroll Lock",
	/* 146 0x-- */	null,
	/* 147 0x-- */	null,
	/* 148 0x-- */	null,
	/* 149 0x-- */	null,
	/* 150 0x-- */	null,
	/* 151 0x-- */	null,
	/* 152 0x-- */	null,
	/* 153 0x-- */	null,
	/* 154 0x-- */	null,
	/* 155 0x-- */	null,
	/* 156 0x-- */	null,
	/* 157 0x-- */	null,
	/* 158 0x-- */	null,
	/* 159 0x-- */	null,
	/* 160 0xA0 */	"Left Shift",
	/* 161 0xA1 */	"Right Shift",
	/* 162 0xA2 */	"Left Control",
	/* 163 0xA3 */	"Right Control",
	/* 164 0xA4 */	"Left Menu",
	/* 165 0xA5 */	"Right Menu",
	/* 166 0xA6 */	"VK_BROWSER_BACK",
	/* 167 0xA7 */	"VK_BROWSER_FORWARD",
	/* 168 0xA8 */	"VK_BROWSER_REFRESH",
	/* 169 0xA9 */	"VK_BROWSER_STOP",
	/* 170 0xAA */	"VK_BROWSER_SEARCH",
	/* 171 0xAB */	"VK_BROWSER_FAVORITES",
	/* 172 0xAC */	"VK_BROWSER_HOME",
	/* 173 0xAD */	"VK_VOLUME_MUTE",
	/* 174 0xAE */	"VK_VOLUME_DOWN",
	/* 175 0xAF */	"VK_VOLUME_UP",
	/* 176 0xB0 */	"VK_MEDIA_NEXT_TRACK",
	/* 177 0xB1 */	"VK_MEDIA_PREV_TRACK",
	/* 178 0xB2 */	"VK_MEDIA_STOP",
	/* 179 0xB3 */	"VK_MEDIA_PLAY_PAUSE",
	/* 180 0xB4 */	"VK_LAUNCH_MAIL",
	/* 181 0xB5 */	"VK_LAUNCH_MEDIA_SELECT",
	/* 182 0xB6 */	"VK_LAUNCH_APP1",
	/* 183 0xB7 */	"VK_LAUNCH_APP2",
	/* 184 0x-- */	null,
	/* 185 0x-- */	null,
	/* 186 0xBA */	"VK_OEM_1",        // ;:
	/* 187 0xBB */	"VK_OEM_PLUS",     // =+
	/* 188 0xBC */	"VK_OEM_COMMA",    // ,
	/* 189 0xBD */	"VK_OEM_MINUS",    // -_
	/* 190 0xBE */	"VK_OEM_PERIOD",   // .
	/* 191 0xBF */	"VK_OEM_2",        // /?
	/* 192 0xC0 */	"VK_OEM_3",        // `~
	/* 193 0x-- */	null,
	/* 194 0x-- */	null,
	/* 195 0x-- */	null,
	/* 196 0x-- */	null,
	/* 197 0x-- */	null,
	/* 198 0x-- */	null,
	/* 199 0x-- */	null,
	/* 200 0x-- */	null,
	/* 201 0x-- */	null,
	/* 202 0x-- */	null,
	/* 203 0x-- */	null,
	/* 204 0x-- */	null,
	/* 205 0x-- */	null,
	/* 206 0x-- */	null,
	/* 207 0x-- */	null,
	/* 208 0x-- */	null,
	/* 209 0x-- */	null,
	/* 210 0x-- */	null,
	/* 211 0x-- */	null,
	/* 212 0x-- */	null,
	/* 213 0x-- */	null,
	/* 214 0x-- */	null,
	/* 215 0x-- */	null,
	/* 216 0x-- */	null,
	/* 217 0x-- */	null,
	/* 218 0x-- */	null,
	/* 219 0xDB */	"VK_OEM_4", // [{
	/* 220 0xDC */	"VK_OEM_5", // \|
	/* 221 0xDD */	"VK_OEM_6", // ]}
	/* 222 0xDE */	"VK_OEM_7", //"'
	/* 223 0xDF */	"VK_OEM_8",
	/* 224 0x-- */	null,
	/* 225 0x-- */	null,
	/* 226 0xE2 */	"VK_OEM_102",
	/* 227 0x-- */	null,
	/* 228 0x-- */	null,
	/* 229 0xE5 */	"VK_PROCESSKEY",
	/* 230 0x-- */	null,
	/* 231 0xE7 */	"VK_PACKET",
	/* 232 0x-- */	null,
	/* 233 0x-- */	null,
	/* 234 0x-- */	null,
	/* 235 0x-- */	null,
	/* 236 0x-- */	null,
	/* 237 0x-- */	null,
	/* 238 0x-- */	null,
	/* 239 0x-- */	null,
	/* 240 0x-- */	null,
	/* 241 0x-- */	null,
	/* 242 0x-- */	null,
	/* 243 0x-- */	null,
	/* 244 0x-- */	null,
	/* 245 0x-- */	null,
	/* 246 0xF6 */	"VK_ATTN",
	/* 247 0xF7 */	"VK_CRSEL",
	/* 248 0xF8 */	"VK_EXSEL",
	/* 249 0xF9 */	"VK_EREOF",
	/* 250 0xFA */	"Play",
	/* 251 0xFB */	"Zoom",
	/* 252 0xFC */	"VK_NONAME",
	/* 253 0xFD */	"VK_PA1",
	/* 254 0xFE */	"VK_OEM_CLEAR",
					null];
