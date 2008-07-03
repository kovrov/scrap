import win32gui
import win32con
import win32api

def wnd_proc(hwnd, message, wparam, lparam):
	if message == win32con.WM_DESTROY:
		win32gui.PostQuitMessage(0)
		return 0
	return win32gui.DefWindowProc(hwnd, message, wparam, lparam)

def winmain(hinstance):
	wndClass = win32gui.WNDCLASS()
	wndClass.lpfnWndProc   = wnd_proc
	wndClass.hInstance     = hinstance
	wndClass.lpszClassName = "className"
	wndClassAtom = win32gui.RegisterClass(wndClass)

	style = win32con.WS_OVERLAPPEDWINDOW
	x = y = win32con.CW_USEDEFAULT
	width = height = win32con.CW_USEDEFAULT
	hwnd = win32gui.CreateWindow(wndClassAtom, "windowTitle", style, x,y, width,height, 0,0, hinstance, None)

	win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
	win32gui.UpdateWindow(hwnd)

	#GdiplusStartup
	win32gui.PumpMessages()
	#GdiplusShutdown

if __name__ == "__main__":
	hinstance = win32api.GetModuleHandle(None)
	winmain(hinstance)
