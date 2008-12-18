/* UI drawing routines using Microsoft Windows Graphics Device Interface
   http://msdn.microsoft.com/library/ms534906 */


// inject "panit" methods into widget hierarchy
static import widget;


template paint_simple_widget()
{
	static import win32 = win32.windows;
	/*override*/
	void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.COLORREF color = win32.GetSysColor(win32.COLOR_APPWORKSPACE);
		win32.HBRUSH hbrush = win32.CreateSolidBrush(color);
		win32.FillRect(hdc, &rect, hbrush);
	}
}
alias widget.Widget!(paint_simple_widget) Widget;


template paint_simple_window()
{
	/*override*/
	void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.COLORREF color = win32.GetSysColor(win32.COLOR_3DFACE);
		win32.HBRUSH hbrush = win32.CreateSolidBrush(color);
		win32.FillRect(hdc, &rect, hbrush);

		win32.DrawEdge(hdc, &rect, win32.EDGE_RAISED, win32.BF_RECT);
	}
}
alias widget.Window!(paint_simple_window, Widget) Window;


template paint_group()
{
	/*override*/
	void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.DrawEdge(hdc, &rect, win32.EDGE_ETCHED, win32.BF_RECT);
	}
}
alias widget.Group !(paint_group, Widget) Group;

/*
template paint_radio()
{
	override void paint(win32.HDC hdc)
	{
		win32.HGDIOBJ old_gdiobj = win32.SelectObject(hdc, win32.GetStockObject(win32.NULL_BRUSH));
		win32.Rectangle(hdc, pos.x, pos.y, pos.x + this.width, pos.y + this.height);
		win32.SelectObject(hdc, old_gdiobj);
	}
}
*/

template paint_button()
{
	/*override*/
	void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.COLORREF color = win32.GetSysColor(win32.COLOR_3DFACE);
		win32.HBRUSH hbrush = win32.CreateSolidBrush(color);
		win32.FillRect(hdc, &rect, hbrush);

		win32.DrawEdge(hdc, &rect, win32.EDGE_RAISED, win32.BF_RECT);
	}
}
alias widget.Button!(paint_button, Widget) Button;

/*
template paint_label()
{
	override void paint(win32.HDC hdc) {}
}
*/

template paint_dialog()
{
	/*override*/
	void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.COLORREF color = win32.GetSysColor(win32.COLOR_3DFACE);
		win32.HBRUSH hbrush = win32.CreateSolidBrush(color);
		win32.FillRect(hdc, &rect, hbrush);

		win32.DrawEdge(hdc, &rect, win32.EDGE_RAISED, win32.BF_RECT);
	}
}
alias widget.Dialog!(paint_dialog, Widget) Dialog;


alias widget.Radio !(paint_simple_widget, Widget) Radio;
alias widget.Label !(paint_simple_widget, Widget) Label;

/*
	void redraw(win32.HWND hwnd)
	{
		win32.HDC hdc = win32.GetDC(hwnd);
		win32.RECT rc;
		win32.GetClientRect(hwnd, &rc);
		offscreen_draw(hdc, &rc);
		win32.ReleaseDC(hwnd, hdc);
	}
*/

static import ui;
static import sys;

template paint_events()
{
	static import win32 = win32.windows;
	static import gdi;

	void on_paint(win32.HWND hwnd)
	{
		win32.PAINTSTRUCT ps;
		win32.HDC hdc = win32.BeginPaint(hwnd, &ps);
		offscreen_draw(hdc, &ps.rcPaint);
		win32.EndPaint(hwnd, &ps);
	}

	void offscreen_draw(win32.HDC hdc, win32.RECT* rect)
	{
		// http://msdn.microsoft.com/library/ms969905
		win32.HDC buffer_dc = win32.CreateCompatibleDC(hdc);
		win32.HBITMAP bitmap = win32.CreateCompatibleBitmap(hdc, rect.right, rect.bottom);
		win32.HBITMAP old_bitmap = win32.SelectObject(buffer_dc, bitmap);
		foreach_reverse(ref node; root)
			(cast(gdi.Widget)node).paint(buffer_dc);
		win32.BitBlt(hdc, 0, 0, rect.right, rect.bottom, buffer_dc, 0, 0, win32.SRCCOPY);
		win32.SelectObject(buffer_dc, old_bitmap);
		win32.DeleteObject(bitmap);
		win32.DeleteDC(buffer_dc);
	}
}
alias ui.IoManager!(paint_events) IoManager;
alias sys.Window!(IoManager) SysWindow;
