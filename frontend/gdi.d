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
}*/
alias widget.Radio !(paint_simple_widget, Widget) Radio;


template paint_button()
{
	static extern (Windows)
	win32.BOOL DrawStateProc(win32.HDC hdc, win32.LPARAM lData, win32.WPARAM wData, int cx, int cy)
	{
		auto rect = win32.RECT(0, 0, cx, cy);
		auto flags = win32.DT_WORDBREAK | win32.DT_EDITCONTROL;
		win32.DrawTextEx(hdc, cast(char*)lData, wData, &rect, flags, null);
		return win32.TRUE;
	}
	/*override*/
	void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.DrawEdge(hdc, &rect,
					win32.EDGE_RAISED, //win32.EDGE_SUNKEN,
					win32.BF_RECT|win32.BF_ADJUST);  // BF_ADJUST will change the rect values

		auto color = win32.GetSysColor(win32.COLOR_3DFACE);
		auto hbrush = win32.CreateSolidBrush(color);
		win32.FillRect(hdc, &rect, hbrush);

		win32.SetBkColor(hdc, win32.GetSysColor(win32.COLOR_3DFACE));
		win32.SetTextColor(hdc, win32.GetSysColor(win32.COLOR_BTNTEXT));

		win32.NONCLIENTMETRICS ncmetrics;
		win32.SystemParametersInfo(win32.SPI_GETNONCLIENTMETRICS, ncmetrics.sizeof, &ncmetrics, 0);
		auto font = win32.CreateFontIndirect(&ncmetrics.lfMessageFont);
		auto old_gdiobj = win32.SelectObject(hdc, font);

		win32.DrawState(hdc, null,
					&DrawStateProc, cast(win32.LPARAM)(this.name.ptr), cast(win32.WPARAM)(this.name.length),
					rect.left, rect.top, rect.right, rect.bottom,
					0);  // win32.DSS_DISABLED

		win32.SelectObject(hdc, old_gdiobj);
		win32.DeleteObject(font);
	}
}
alias widget.Button!(paint_button, Widget) Button;

/*
template paint_label()
{
	override void paint(win32.HDC hdc) {}
}*/
alias widget.Label !(paint_simple_widget, Widget) Label;


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
