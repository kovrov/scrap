/* system is platform-specific routines */

module system;

static import renderer;
version (Windows)
{
	static import win32 = win32.windows;
}

public import system_keys;
static import std.string;

/// _Window subsystem properties. accesible via system.window
struct WindowSettings
{
	/// application window _title property
	string title;
	/// width and height of application window or sceen
	void size(uint i, uint j) { width = i, height = j; }
	uint width = 640; /// ditto
	uint height = 480; /// ditto
	/// full-screen toggler
	bool fullscreen() { return _fullscreen; }
	bool fullscreen(bool set)
	{
		if (_fullscreen == set) return set;
		_settings_touched = true;
		return _fullscreen = set;
	}
	/// resizeble window property
	bool resizable = true;
	/// trap mouse cursor property
	bool trap_cursor = false;

private:
	bool _fullscreen = false;
	bool _settings_touched = false;
}
/// interface to access global Window
WindowSettings window;


/// interface to access system.window properties
struct Timer
{
	double total;
	double game;
	double frame;
	bool pause = false;
}
/// system.timer interface
Timer timer;


struct Input
{
	struct M { long x, y; } M mouse;
	bool[256] keyboard;
}
/// system.input interface
Input input;


/// system interface
bool active = true;


/// main loop
int run(void function () game_tick)
in
{
	assert (game_tick, "game_tick must be provided");
}
body
{
	_init();

	win32.MSG msg;
	while (true)
	{
		/*	This is important to check if there was a message
			before proceed with game tick */
		if (win32.PeekMessage(&msg, null, 0, 0, win32.PM_REMOVE))
        {
			if (msg.message == win32.WM_QUIT)  // WM_CLOSE or system.exit()
				break;
            win32.TranslateMessage(&msg);  // Find out what the message does
            win32.DispatchMessage(&msg);  // Execute the message (WinProc)
        }
		else
		{
			if (window._settings_touched)
			{
				window._settings_touched = false;
				_initScreenMode(window._fullscreen, 32);
			}

			_updateLastFrameTime();

			// save some cpu cycles if we got more than 60 fps
			if (timer.frame < 0.016) win32.Sleep(16 - cast(int)(timer.frame * 1000));

			game_tick();
			renderer.swapBuffers();
		}
	}

	_shutdown();

	return (msg.wParam);  // Return from the program
}


/// application sutdown
void exit(int exit_code=0)
{
	version (Windows)
	{
		win32.PostQuitMessage(exit_code);
	}
}




// internal stuff
private:

bool _use_raw_input = false;
long _cpu_freq;
bool _render_initialized = false;
uint _fps;
win32.HWND _hwnd;

debug import std.stdio;

extern (Windows)
int _windowProcCallback(win32.HWND hWnd, uint msg, win32.WPARAM wParam, win32.LPARAM lParam)
{
    switch (msg)
	{
	case win32.WM_INPUT: // http://msdn2.microsoft.com/library/ms645590
		{
			static win32.RAWINPUT raw;
			uint dwSize = win32.RAWINPUT.sizeof;
			win32.GetRawInputData(cast(win32.HRAWINPUT)lParam, win32.RID_INPUT, &raw, &dwSize, win32.RAWINPUTHEADER.sizeof);
			if (raw.header.dwType == win32.RIM_TYPEMOUSE)
			{
				//if (raw.data.mouse.usFlags & win32.MOUSE_MOVE_RELATIVE)
				//if (raw.data.mouse.usFlags & win32.MOUSE_MOVE_ABSOLUTE)
				input.mouse.x = raw.data.mouse.lLastX;
				input.mouse.y = 0 - raw.data.mouse.lLastY;
			}
			else if (raw.header.dwType == win32.RIM_TYPEKEYBOARD)
			{
				if (raw.data.keyboard.Message == win32.WM_KEYDOWN || raw.data.keyboard.Message == win32.WM_SYSKEYDOWN)
				{
					input.keyboard[raw.data.keyboard.VKey] = true;
					debug writefln("WM_INPUT: ", KEY_NAMES[raw.data.keyboard.VKey]);
				}
				else if (raw.data.keyboard.Message == win32.WM_KEYUP || raw.data.keyboard.Message == win32.WM_SYSKEYUP)
				{
					input.keyboard[raw.data.keyboard.VKey] = false;
				}
			}
		}
		break;  // application must call DefWindowProc so the system can perform cleanup.

	case win32.WM_KEYDOWN:
		if (_use_raw_input) return 0;
		input.keyboard[wParam] = true;
		break;
	case win32.WM_KEYUP:
		if (_use_raw_input) return 0;
		input.keyboard[wParam] = false;
		break;
	case win32.WM_MOUSEMOVE:
		if (_use_raw_input) return 0;
		debug writefln("WM_MOUSEMOVE");
		break;

    case win32.WM_SIZE:  // If the window is resized
		debug writefln("WM_SIZE (%d, %d)", win32.LOWORD(lParam), win32.HIWORD(lParam));
		if (_render_initialized)
			renderer.resizeViewport(win32.LOWORD(lParam), win32.HIWORD(lParam));
        return 0;

	case win32.WM_ACTIVATE:  // main window minimization/restore
		active = !win32.HIWORD(wParam);
		debug writefln("WM_ACTIVATE %s", active);
		break;

    case win32.WM_CLOSE:
        win32.PostQuitMessage(0);
        break;

	default: // oh, D!
	}

    return win32.DefWindowProc(hWnd, msg, wParam, lParam);
}


/*
	See "Taking Advantage of High-Definition Mouse Movement"
		http://msdn2.microsoft.com/library/bb206183
*/
void _initInput(win32.HWND hWnd)
{
	//  register raw input
	win32.RAWINPUTDEVICE rid[2]; // http://msdn2.microsoft.com/library/ms645565

	rid[0].usUsagePage = 0x01;  //HID_USAGE_PAGE_GENERIC
	rid[0].usUsage = 0x02;  //HID_USAGE_GENERIC_MOUSE
//	rid[0].dwFlags = win32.RIDEV_NOLEGACY;  // RIDEV_CAPTUREMOUSE | RIDEV_INPUTSINK
	rid[0].hwndTarget = hWnd;

	rid[1].usUsagePage = 0x01;  //HID_USAGE_PAGE_GENERIC
	rid[1].usUsage = 0x06;  //HID_USAGE_GENERIC_KEYBOARD
	rid[1].dwFlags = win32.RIDEV_NOLEGACY|win32.RIDEV_NOHOTKEYS|win32.RIDEV_APPKEYS;  // RIDEV_INPUTSINK
	rid[1].hwndTarget = hWnd;

	win32.RegisterRawInputDevices(rid.ptr, 2, win32.RAWINPUTDEVICE.sizeof); // WinXP only =(
	_use_raw_input = true;
}



void _updateLastFrameTime()
in
{
	assert (_cpu_freq, "high-resolution performance must be supported!");
}
body
{
	static long prev;
	static long tics_count;
	static uint frames_count;
	win32.LARGE_INTEGER cur;
	assert (win32.QueryPerformanceCounter(&cur), "win32.QueryPerformanceCounter() failed");
	timer.frame = (cur.QuadPart - prev) / cast(double)_cpu_freq; // time in seconds

	++frames_count;
	tics_count += (cur.QuadPart - prev);
	if (tics_count > _cpu_freq)
	{
		_fps = frames_count;
		frames_count = 0;
		tics_count = 0;
		win32.SetWindowText(_hwnd, (window.title ~ " - " ~ std.string.toString(_fps) ~ " FPS").ptr);
	}
	prev = cur.QuadPart;
}


// platform-specific initialize routines
version (Windows)
void _init()
{
	// set up timer
	win32.LARGE_INTEGER freq;
	if (win32.QueryPerformanceFrequency(&freq) != 0) // should be used every time?
		_cpu_freq = freq.QuadPart;

	// TODO: change screen mode may fail righteously...
	_initScreenMode(window._fullscreen, 32);  // may throw

	// initialize window
	_hwnd = _initAppWindow(window.width, window.height, window.title);
	window._settings_touched = false;

	// initialize render
	renderer.init(_hwnd, 32);
	renderer.resizeViewport(window.width, window.height);
	_render_initialized = true; // this is for premature WM_SIZE

	// initialize input
	_initInput(_hwnd);
}


void _shutdown()
{
	renderer.shutdown();
	_render_initialized = false;
	// destroyWindow
}


win32.HWND _initAppWindow(int width, int height, string app_title)
{
	// 1. register "window class"
	win32.WNDCLASS wndclass;
	wndclass.style = win32.CS_HREDRAW | win32.CS_VREDRAW;
	wndclass.lpfnWndProc = &_windowProcCallback;
	wndclass.hInstance = win32.GetModuleHandle(null);
	wndclass.hIcon = win32.LoadIcon(null, win32.IDI_APPLICATION);
	wndclass.hCursor = win32.LoadCursor(null, win32.IDC_ARROW);
	wndclass.hbrBackground = null; // no backgrounde erase
	wndclass.lpszClassName = "gimbal_window";
	win32.RegisterClass(&wndclass);  // TODO: validate

	// 3. create window
	win32.DWORD style;
	win32.DWORD ext_style;

	if (window._fullscreen)
	{
		ext_style = win32.WS_EX_APPWINDOW;
		style = win32.WS_POPUP;
	}
	else
	{
		ext_style = win32.WS_EX_APPWINDOW | win32.WS_EX_WINDOWEDGE;
		style = win32.WS_OVERLAPPEDWINDOW;
	}

	win32.RECT wnd_rect;  // note, D always initialize variables
	wnd_rect.right	= window.width;
	wnd_rect.bottom	= window.height;

	// Adjust Window To True Requested Size
	win32.AdjustWindowRect(&wnd_rect, style, false);

	// Actual "create window" part
	_hwnd = win32.CreateWindow("gimbal_window", app_title.ptr, style,
									win32.CW_USEDEFAULT, win32.CW_USEDEFAULT,
									wnd_rect.right - wnd_rect.left, wnd_rect.bottom - wnd_rect.top, 
									null, null, wndclass.hInstance, null);
	if (!_hwnd)
		throw new Exception("win32.CreateWindow failed");

	win32.ShowWindow(_hwnd, win32.SW_SHOWNORMAL);
	//win32.UpdateWindow(_hwnd);
	win32.SetFocus(_hwnd);
	win32.SetForegroundWindow(_hwnd);  // Slightly Higher Priority

	return _hwnd;
}


void _initScreenMode(bool fullscreen, int bits)
{
	if (!fullscreen)
	{
		win32.ChangeDisplaySettings(null, 0);
		return;
	}

	win32.DEVMODE screen_settings;  // Device Mode
	screen_settings.dmSize = win32.DEVMODE.sizeof;  // Size of DEVMODE struct
	screen_settings.dmPelsWidth = window.width;  // Selected Screen Width
	screen_settings.dmPelsHeight = window.height;  // Selected Screen Height
	screen_settings.dmBitsPerPel = bits;  // Selected Bits Per Pixel
	screen_settings.dmFields = win32.DM_BITSPERPEL | win32.DM_PELSWIDTH | win32.DM_PELSHEIGHT;

	// Try To Set Selected Mode And Get Results.
	// NOTE: CDS_FULLSCREEN Gets Rid Of Start Bar.
	if (win32.ChangeDisplaySettings(&screen_settings, win32.CDS_FULLSCREEN)
				!= win32.DISP_CHANGE_SUCCESSFUL)
	{
		throw new Exception("Requested mode is not supported");
	}
}
