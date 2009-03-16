import win32api, win32gui, win32con

szTitle = "wintest"
szWindowClass = "WINTEST"

def OnDestroy(hwnd, msg, wp, lp):
	print "OnDestroy"
	win32gui.PostQuitMessage(0)

def OnPaint(hwnd, msg, wp, lp):
	print "OnPaint"
	dc,ps = win32gui.BeginPaint(hwnd)
	# TODO: Add any drawing code here...
	win32gui.EndPaint(hwnd, ps)
	return 0

def main():
	# register window class
	wc = win32gui.WNDCLASS()
	wc.lpszClassName = szWindowClass
	wc.style = win32con.CS_GLOBALCLASS | win32con.CS_VREDRAW | win32con.CS_HREDRAW
	wc.hbrBackground = win32con.COLOR_WINDOW+1
	wc.lpfnWndProc = {
		win32con.WM_PAINT: OnPaint,
		win32con.WM_DESTROY: OnDestroy }
	class_atom = win32gui.RegisterClass(wc)
	print class_atom
	# create window
	hWnd = win32gui.CreateWindowEx(0,                            # dwExStyle
	                               class_atom, szTitle,          # className,windowTitle,
								   win32con.WS_OVERLAPPEDWINDOW, # style
								   win32con.CW_USEDEFAULT,0,     # x,y
								   win32con.CW_USEDEFAULT,0,     # width,height
								   0,							 # parent
								   0,							 # menu
								   win32api.GetModuleHandle(None),# hinstance
								   None)						 # reserved
	win32gui.ShowWindow(hWnd, win32con.SW_SHOWNORMAL)
	win32gui.UpdateWindow(hWnd)
	# Main message loop:
	while True:
		res,msg = win32gui.GetMessage(0, 0, 0)
		win32gui.TranslateMessage(msg)
		win32gui.DispatchMessage(msg)
		if res == 0:
			break
	return msg[2]

if __name__ == "__main__": main()
