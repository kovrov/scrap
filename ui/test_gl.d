void main()
{
/*
	init:
	* create application window (RegisterClass/CreateWindow)
	* set pixel format (ChoosePixelFormat/SetPixelFormat)
	* create rendering context (wglCreateContext/wglMakeCurrent)
	* initialize input

	loop:
	* pump messages (PeekMessage/DispatchMessage)
	* call user update callback
	* draw:
		* clear buffer (glClear)
		* call user draw callback
		* swap buffers (SwapBuffers)

	shutdown:
	* ...
*/
}


// http://msdn.microsoft.com/library/ms632593
// http://msdn.microsoft.com/library/ms633573
extern (Windows)
win32.LRESULT window_procedure(win32.HWND hWnd, uint msg, win32.WPARAM wParam, win32.LPARAM lParam)
{
    switch (msg)
	{
	case win32.WM_INPUT:  // http://msdn.microsoft.com/library/ms645590
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
