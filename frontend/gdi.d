/* Drawing routines using Microsoft Windows "Graphics Device Interface" */

static import win32 = win32.windows;
pragma(lib, "win32.lib");

void paint_handler(void delegate(win32.HDC hdc) paint_handler)
{
	win32.PAINTSTRUCT ps;
	win32.HDC hdc = win32.BeginPaint(hWnd, &ps);
	offScreenDraw(hdc, &ps.rcPaint, paint_handler);
	win32.EndPaint(hWnd, &ps);
}

void redraw(void delegate(win32.HDC hdc) paint_handler)
{
	win32.HDC hdc = win32.GetDC(this.handle);
	win32.RECT rc;
	win32.GetClientRect(this.handle, &rc);
	offscreen_draw(hdc, &rc, this.paint_handler);
	win32.ReleaseDC(this.handle, hdc);
}

void offscreen_draw(win32.HDC hdc, win32.RECT* rect, void delegate(win32.HDC hdc) paint_handler)
{
	// http://msdn.microsoft.com/library/ms969905
	win32.HDC buffer_dc = win32.CreateCompatibleDC(hdc);
	win32.HBITMAP bitmap = win32.CreateCompatibleBitmap(hdc, rect.right, rect.bottom);
	win32.HBITMAP old_bitmap = win32.SelectObject(buffer_dc, bitmap);
	paint_handler(buffer_dc);
	win32.BitBlt(hdc, 0, 0, rect.right, rect.bottom, buffer_dc, 0, 0, win32.SRCCOPY);
	win32.SelectObject(buffer_dc, old_bitmap);
	win32.DeleteObject(bitmap);
	win32.DeleteDC(buffer_dc);
}
