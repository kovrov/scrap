import win32api, win32gui, win32con

def OnDestroy(hwnd, msg, wp, lp):
	print "OnDestroy"
	win32gui.PostQuitMessage(0)

def OnPaint(hwnd, msg, wp, lp):
	print "OnPaint"
	dc,ps = win32gui.BeginPaint(hwnd)
	# TODO: Add drawing code here...
	win32gui.EndPaint(hwnd, ps)
	return 0

def register_wndclass():
	wc = win32gui.WNDCLASS()
	wc.lpszClassName = "WINTEST"
	wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
	wc.hbrBackground = win32con.COLOR_WINDOW+1
	wc.lpfnWndProc = {
		win32con.WM_PAINT: OnPaint,
		win32con.WM_DESTROY: OnDestroy }
	return win32gui.RegisterClass(wc)

def create_window(class_atom, title):
	hWnd = win32gui.CreateWindow(class_atom, title,            # className,windowTitle,
								 win32con.WS_OVERLAPPEDWINDOW, # style
								 win32con.CW_USEDEFAULT,0,     # x,y
								 win32con.CW_USEDEFAULT,0,     # width,height
								 0,                            # parent
								 0,                            # menu
								 win32api.GetModuleHandle(None),# hinstance
								 None)                         # reserved
	win32gui.ShowWindow(hWnd, win32con.SW_SHOWNORMAL)
	win32gui.UpdateWindow(hWnd)

def main():
	class_atom = register_wndclass()
	create_window(class_atom, "pywin32 test")
	while True:
		res,msg = win32gui.GetMessage(0, 0, 0)
		if res == 0:
			break
		win32gui.TranslateMessage(msg)
		win32gui.DispatchMessage(msg)
	return msg[2]

if __name__ == "__main__": main()
