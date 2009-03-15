import win32con
from ctypes import *
from ctypes import wintypes
import win32gui


# windows api boilerplate
CreateWindowEx = windll.user32.CreateWindowExW
CreateWindowEx.argtypes = [wintypes.DWORD,
                           wintypes.LPCWSTR,
                           wintypes.LPCWSTR,
                           wintypes.DWORD,
                           c_int, c_int, c_int, c_int, 
                           wintypes.HWND,
                           wintypes.HMENU,
                           wintypes.HINSTANCE,
                           wintypes.LPVOID]
def ErrorIfZero(handle):
	if handle == 0:
		raise Exception("CreateWindowEx failed")
	else:
		return handle
CreateWindowEx.restype = ErrorIfZero

# LRESULT is defined as LONG_PTR (signed type)
if sizeof(c_int32) == sizeof(c_void_p):
    LRESULT = c_int32
elif sizeof(c_int64) == sizeof(c_void_p):
    LRESULT = c_int64
WNDPROC = WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)


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

RegisterClass = windll.user32.RegisterClassW
RegisterClass.argtypes = [POINTER(WNDCLASS)]
RegisterClass.restype = wintypes.ATOM

class PAINTSTRUCT(Structure):
	_fields_ = [('hdc', c_int),
	            ('fErase', c_int),
	            ('rcPaint', wintypes.RECT),
	            ('fRestore', c_int),
	            ('fIncUpdate', c_int),
	            ('rgbReserved', c_char * 32)]

hInst = None  # current instance
szTitle = "wintest"
szWindowClass = "WINTEST"

def main():
	hInstance = windll.kernel32.GetModuleHandleW(c_int(win32con.NULL))
	MyRegisterClass(hInstance)
	# Perform application initialization:
	InitInstance(hInstance, win32con.SW_SHOWNORMAL)
	# Main message loop:
	msg = wintypes.MSG()
	pMsg = pointer(msg)
	NULL = c_int(win32con.NULL)
	while windll.user32.GetMessageW(pMsg, NULL, 0, 0) != 0:
		windll.user32.TranslateMessage(pMsg)
		windll.user32.DispatchMessageW(pMsg)
	return msg.wParam



"""
FUNCTION: MyRegisterClass()

PURPOSE: Registers the window class.

COMMENTS:

	This function and its usage are only necessary if you want this code
	to be compatible with Win32 systems prior to the 'RegisterClassEx'
	function that was added to Windows 95. It is important to call this function
	so that the application will get 'well formed' small icons associated
	with it.
"""
def MyRegisterClass(hInstance):
	#---------------
	# Define Window Class
	wndclass = WNDCLASS() # win32gui.WNDCLASS()
	wndclass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
	wndclass.lpfnWndProc = WNDPROC(WndProc)
	#wndclass.cbClsExtra = wndclass.cbWndExtra = 0
	wndclass.hInstance = hInstance
	wndclass.hIcon = windll.user32.LoadIconW(c_int(win32con.NULL), c_int(win32con.IDI_APPLICATION))
	wndclass.hCursor = windll.user32.LoadCursorW(c_int(win32con.NULL), c_int(win32con.IDC_ARROW))
	wndclass.hbrBackground = windll.gdi32.GetStockObject(c_int(win32con.WHITE_BRUSH))
	wndclass.lpszMenuName = ""
	wndclass.lpszClassName = szWindowClass
	# Register Window Class
	#if not win32gui.RegisterClass(wndclass):
	if not RegisterClass(byref(wndclass)):
		raise Exception()

"""
FUNCTION: InitInstance(HINSTANCE, int)

PURPOSE: Saves instance handle and creates main window

COMMENTS:

	In this function, we save the instance handle in a global variable and
	create and display the main program window.
"""
def InitInstance(hInstance, nCmdShow):
	global hInst
	hInst = hInstance  # Store instance handle in our global variable
	#hWnd = win32gui.CreateWindowEx(0, szWindowClass, szTitle,
	hWnd = CreateWindowEx(0, szWindowClass, szTitle,
	                               win32con.WS_OVERLAPPEDWINDOW,
	                               win32con.CW_USEDEFAULT, 0,
	                               win32con.CW_USEDEFAULT, 0,
	                               win32con.NULL,
	                               win32con.NULL,
	                               hInstance,
	                               None)
	if hWnd == 0:
		raise Exception()
	windll.user32.ShowWindow(c_int(hWnd), c_int(nCmdShow))
	windll.user32.UpdateWindow(c_int(hWnd))
	return True

"""
FUNCTION: WndProc(HWND, UINT, WPARAM, LPARAM)

PURPOSE:  Processes messages for the main window.

WM_COMMAND	- process the application menu
WM_PAINT	- Paint the main window
WM_DESTROY	- post a quit message and return
"""
def WndProc(hWnd, message, wParam, lParam):
	ps = PAINTSTRUCT()
	rect = wintypes.RECT()
	if message == win32con.WM_PAINT:
		hdc = windll.user32.BeginPaint(c_int(hWnd), byref(ps))
		# TODO: Add any drawing code here...
		windll.user32.EndPaint(c_int(hWnd), byref(ps))
	elif message == win32con.WM_DESTROY:
		windll.user32.PostQuitMessage(0)
	else:
		return windll.user32.DefWindowProcW(c_int(hWnd), c_int(message), c_int(wParam), c_int(lParam))
	return 0


#-------------------------------------------------------------------------------


if __name__ == "__main__": main()
