/* Drawing routines using Microsoft Windows "Graphics Device Interface" */

template paint_events()
{
	static import win32 = win32.windows;

	void on_paint(win32.HWND hwnd)
	{
		win32.PAINTSTRUCT ps;
		win32.HDC hdc = win32.BeginPaint(hwnd, &ps);
		offscreen_draw(hdc, &ps.rcPaint);
		win32.EndPaint(hwnd, &ps);
	}

	static void offscreen_draw(win32.HDC hdc, win32.RECT* rect)
	{
		// http://msdn.microsoft.com/library/ms969905
		win32.HDC buffer_dc = win32.CreateCompatibleDC(hdc);
		win32.HBITMAP bitmap = win32.CreateCompatibleBitmap(hdc, rect.right, rect.bottom);
		win32.HBITMAP old_bitmap = win32.SelectObject(buffer_dc, bitmap);
//		GDI_PAINT(buffer_dc);
		win32.BitBlt(hdc, 0, 0, rect.right, rect.bottom, buffer_dc, 0, 0, win32.SRCCOPY);
		win32.SelectObject(buffer_dc, old_bitmap);
		win32.DeleteObject(bitmap);
		win32.DeleteDC(buffer_dc);
	}
}





template paint_simple_window()
{
	static import win32 = win32.windows;

	/*override*/ void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		win32.Rectangle(hdc,
				pos.x, pos.y,
				pos.x + this.width, pos.y + this.height);
	}
}

template gdi_paint_group()
{
	override void paint(win32.HDC hdc) {}
}

template gdi_paint_radio()
{
	override void paint(win32.HDC hdc) {}
}

template gdi_paint_button()
{
	override void paint(win32.HDC hdc) {}
}

template gdi_paint_label()
{
	override void paint(win32.HDC hdc) {}
}

template gdi_paint_dialog()
{
	override void paint(win32.HDC hdc) {}
}


/*
template paint(alias GDI_PAINT)
{
	static import win32 = win32.windows;

	void on_paint(win32.HWND hwnd)
	{
		win32.PAINTSTRUCT ps;
		win32.HDC hdc = win32.BeginPaint(hwnd, &ps);
		offscreen_draw(hdc, &ps.rcPaint);
		win32.EndPaint(hwnd, &ps);
	}

	void redraw(win32.HWND hwnd)
	{
		win32.HDC hdc = win32.GetDC(hwnd);
		win32.RECT rc;
		win32.GetClientRect(hwnd, &rc);
		offscreen_draw(hdc, &rc);
		win32.ReleaseDC(hwnd, hdc);
	}

	void offscreen_draw(win32.HDC hdc, win32.RECT* rect)
	{
		// http://msdn.microsoft.com/library/ms969905
		win32.HDC buffer_dc = win32.CreateCompatibleDC(hdc);
		win32.HBITMAP bitmap = win32.CreateCompatibleBitmap(hdc, rect.right, rect.bottom);
		win32.HBITMAP old_bitmap = win32.SelectObject(buffer_dc, bitmap);
		GDI_PAINT(buffer_dc);
		win32.BitBlt(hdc, 0, 0, rect.right, rect.bottom, buffer_dc, 0, 0, win32.SRCCOPY);
		win32.SelectObject(buffer_dc, old_bitmap);
		win32.DeleteObject(bitmap);
		win32.DeleteDC(buffer_dc);
	}
}
*/
