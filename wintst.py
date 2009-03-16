import win32con
from ctypes import *
from ctypes import wintypes

# LRESULT is defined as LONG_PTR (signed type)
if sizeof(c_int32) == sizeof(c_void_p):
	print "LRESULT is 32-bit"
	LRESULT = c_int32
elif sizeof(c_int64) == sizeof(c_void_p):
	print "LRESULT is 64-bit"
	LRESULT = c_int64
WNDPROC = WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

class PAINTSTRUCT(Structure):
	_fields_ = [('hdc', c_int),
	            ('fErase', c_int),
	            ('rcPaint', wintypes.RECT),
	            ('fRestore', c_int),
	            ('fIncUpdate', c_int),
	            ('rgbReserved', c_char * 32)]

class WNDCLASS(Structure):
	_fields_ = [('style', wintypes.UINT),
	            ('lpfnWndProc', WNDPROC),
	            ('cbClsExtra', c_int),
	            ('cbWndExtra', c_int),
	            ('hInstance', wintypes.HINSTANCE),
	            ('hIcon', wintypes.HICON),
	            ('hCursor', wintypes.HICON),
	            ('hbrBackground', wintypes.HBRUSH),
	            ('lpszMenuName', wintypes.LPCWSTR),
	            ('lpszClassName', wintypes.LPCWSTR)]

def assert_nonzerro(res):
	if res == 0:
		raise Exception("TODO: ...")
	return res

RegisterClass = windll.user32.RegisterClassW
RegisterClass.argtypes = [POINTER(WNDCLASS)]
RegisterClass.restype = assert_nonzerro

CreateWindowEx = windll.user32.CreateWindowExW
CreateWindowEx.restype = assert_nonzerro
CreateWindowEx.argtypes = [wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR,
                           wintypes.DWORD, c_int, c_int, c_int, c_int, 
                           wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE,
                           wintypes.LPVOID]

def wnd_proc(hWnd, message, wParam, lParam):
	if message == win32con.WM_PAINT:
		ps = PAINTSTRUCT()
		rect = wintypes.RECT()
		hdc = windll.user32.BeginPaint(c_int(hWnd), byref(ps))
		# TODO: Add any drawing code here...
		windll.user32.EndPaint(c_int(hWnd), byref(ps))
	elif message == win32con.WM_DESTROY:
		windll.user32.PostQuitMessage(0)
	else:
		return windll.user32.DefWindowProcW(c_int(hWnd), c_int(message), c_int(wParam), c_int(lParam))
	return 0
WndProc = WNDPROC(wnd_proc)

def register_wndclass():
	wndclass = WNDCLASS()
	wndclass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
	wndclass.lpfnWndProc = WndProc
	wndclass.hInstance = windll.kernel32.GetModuleHandleW(None)
	wndclass.hbrBackground = 0
	wndclass.lpszClassName = u"WINTEST"
	RegisterClass(byref(wndclass))

def create_window(nCmdShow):
	hWnd = CreateWindowEx(0, u"WINTEST", u"втф?",
						  win32con.WS_OVERLAPPEDWINDOW,
						  win32con.CW_USEDEFAULT, 0,
						  win32con.CW_USEDEFAULT, 0,
						  0, 0, windll.kernel32.GetModuleHandleW(None), None)
	windll.user32.ShowWindow(c_int(hWnd), c_int(nCmdShow))
	windll.user32.UpdateWindow(c_int(hWnd))

def main():
	register_wndclass()
	create_window(win32con.SW_SHOWNORMAL)
	msg = wintypes.MSG()
	pMsg = pointer(msg)
	NULL = c_int(win32con.NULL)
	while windll.user32.GetMessageW(pMsg, NULL, 0, 0) != 0:
		windll.user32.TranslateMessage(pMsg)
		windll.user32.DispatchMessageW(pMsg)
	return msg.wParam

if __name__ == "__main__": main()
