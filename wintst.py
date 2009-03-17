from ctypes import *
from ctypes import wintypes


WM_NCCREATE = 0x81
WM_DESTROY = 0x02
CS_VREDRAW = 0x01
CS_HREDRAW = 0x02
WS_OVERLAPPEDWINDOW = 0xCF0000
CW_USEDEFAULT = -0x80000000
SW_SHOWNORMAL = 0x01
FORMAT_MESSAGE_FROM_SYSTEM = 0x1000

# LRESULT is defined as LONG_PTR (signed type)
if sizeof(c_int32) == sizeof(c_void_p): LRESULT = c_int32
elif sizeof(c_int64) == sizeof(c_void_p): LRESULT = c_int64
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

def assert_nonzerro(res):
	if res == 0:
		errno = windll.kernel32.GetLastError()
		message = create_string_buffer(1024)
		windll.kernel32.FormatMessageA(FORMAT_MESSAGE_FROM_SYSTEM,
									   c_void_p(), errno, 0,
									   message, len(message),
									   c_void_p())
		raise Exception(message.value)
	return res

RegisterClass = windll.user32.RegisterClassW
RegisterClass.restype = assert_nonzerro
RegisterClass.argtypes = [POINTER(WNDCLASS)]

CreateWindowEx = windll.user32.CreateWindowExW
CreateWindowEx.restype = assert_nonzerro
CreateWindowEx.argtypes = [wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR,
						   wintypes.DWORD, c_int, c_int, c_int, c_int, 
						   wintypes.HWND, wintypes.HMENU, wintypes.HINSTANCE,
						   wintypes.LPVOID]

DefWindowProc = windll.user32.DefWindowProcW
DefWindowProc.restype = LRESULT
DefWindowProc.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]

GetMessage = windll.user32.GetMessageW
GetMessage.restype = wintypes.BOOL
GetMessage.argtypes = [POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]

DispatchMessage = windll.user32.DispatchMessageW
DispatchMessage.restype = LRESULT
DispatchMessage.argtypes = [POINTER(wintypes.MSG)]

class CREATESTRUCT(Structure):
	_fields_ = [('lpCreateParams', wintypes.LPVOID),
				('hInstance', wintypes.HINSTANCE),
				('hMenu', wintypes.HMENU),
				('hwndParent', wintypes.HWND),
				('cy', c_int),
				('cx', c_int),
				('y', c_int),
				('x', c_int),
				('style', wintypes.LONG),
				('lpszName', wintypes.LPCWSTR),
				('lpszClass', wintypes.LPCWSTR),
				('dwExStyle', wintypes.DWORD)]

#-------------------------------------------------------------------------------

def wnd_proc(hWnd, message, wParam, lParam):
	if message == WM_NCCREATE:
		cs = CREATESTRUCT.from_address(lParam)
		print cs.lpszName
		print cs.lpszClass
		assert 1 == DefWindowProc(hWnd, message, wParam, lParam)
		return 1
	elif message == WM_DESTROY:
		windll.user32.PostQuitMessage(0)
	else:
		return DefWindowProc(hWnd, message, wParam, lParam)
	return 0
WndProc = WNDPROC(wnd_proc)

def main():
	# register wndclass
	wndclass = WNDCLASS()
	wndclass.style = CS_HREDRAW | CS_VREDRAW
	wndclass.lpfnWndProc = WndProc
	wndclass.hInstance = windll.kernel32.GetModuleHandleW(None)
	wndclass.hbrBackground = 1
	wndclass.lpszClassName = u"WINTEST"
	RegisterClass(byref(wndclass))
	# create window
	hWnd = CreateWindowEx(0, u"WINTEST", u"test window", WS_OVERLAPPEDWINDOW,
						  CW_USEDEFAULT, 0, CW_USEDEFAULT, 0,
						  0, 0, windll.kernel32.GetModuleHandleW(None), None)
	windll.user32.ShowWindow(hWnd, SW_SHOWNORMAL)
	windll.user32.UpdateWindow(hWnd)
	# pump messages
	msg = wintypes.MSG()
	pMsg = pointer(msg)
	while GetMessage(pMsg, None, 0, 0):
		#windll.user32.TranslateMessage(pMsg)
		DispatchMessage(pMsg)
	return msg.wParam

if __name__ == "__main__": main()
