/* UI drawing routines using Microsoft Windows Graphics Device Interface
   http://msdn.microsoft.com/library/ms534906 */

pragma(lib, "win32.lib");
static import win32 = win32.windows;
static import sys;
static import ui;
static import widget;


struct Style
{
	win32.COLORREF buttonColor;
	win32.COLORREF buttonTextColor;
	win32.HBRUSH appWorkspace;
	win32.HBRUSH buttonFace;
	win32.HFONT buttonFont;
	void load()
	{
		this.buttonColor = win32.GetSysColor(win32.COLOR_3DFACE);
		this.buttonTextColor = win32.GetSysColor(win32.COLOR_BTNTEXT);

		this.appWorkspace = win32.GetSysColorBrush(win32.COLOR_APPWORKSPACE);
		this.buttonFace = win32.GetSysColorBrush(win32.COLOR_3DFACE);

		win32.NONCLIENTMETRICS nc_metrics;
		win32.SystemParametersInfo(win32.SPI_GETNONCLIENTMETRICS, nc_metrics.sizeof, &nc_metrics, 0);
		this.buttonFont = win32.CreateFontIndirect(&nc_metrics.lfMessageFont);
	}
	~this()
	{
		win32.DeleteObject(this.appWorkspace);
		win32.DeleteObject(this.buttonFace);
		win32.DeleteObject(this.buttonFont);
	}
}
Style style;
static this()
{
	style.load();
}


// inject "panit" interface into widget hierarchy
template node_paint_interface()
{
	static import win32 = win32.windows;
	abstract void paint(win32.HDC hdc);
}
alias ui.io!(node_paint_interface).TargetNode BaseNode;
alias widget.base!(BaseNode) widgets;

template forward_ctor() { this(string name, BaseNode parent=null) { super(name, parent); }}


class Widget : widgets.Widget
{
	mixin forward_ctor;
	override void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.FillRect(hdc, &rect, style.appWorkspace);
	}
}


class Window : widgets.Window
{
	mixin forward_ctor;
	override void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.FillRect(hdc, &rect, style.buttonFace);
		win32.DrawEdge(hdc, &rect, win32.EDGE_RAISED, win32.BF_RECT);
	}
}


class Group : widgets.Group
{
	mixin forward_ctor;
	override void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.DrawEdge(hdc, &rect, win32.EDGE_ETCHED, win32.BF_RECT);
	}
}


class Radio : widgets.Radio
{
	mixin forward_ctor;
	override void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.FillRect(hdc, &rect, style.appWorkspace);
	}
}


class Button : widgets.Button
{
	mixin forward_ctor;
	override void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.DrawEdge(hdc, &rect,
					this.tracked ? win32.EDGE_RAISED : win32.EDGE_SUNKEN,
					win32.BF_RECT|win32.BF_ADJUST);  // BF_ADJUST will change the rect values

		win32.FillRect(hdc, &rect, style.buttonFace);

		win32.SetBkColor(hdc, style.buttonColor);
		win32.SetTextColor(hdc, style.buttonTextColor);
		auto old_gdiobj = win32.SelectObject(hdc, style.buttonFont);
		win32.DrawState(hdc, null,
					&TextDrawStateProc, cast(win32.LPARAM)(this.name.ptr), cast(win32.WPARAM)(this.name.length),
					rect.left, rect.top, rect.right-rect.left, rect.bottom-rect.top,
					0);  // win32.DSS_DISABLED
		win32.SelectObject(hdc, old_gdiobj);
	}
	static extern (Windows)
	win32.BOOL TextDrawStateProc(win32.HDC hdc, win32.LPARAM lData, win32.WPARAM wData, int cx, int cy)
	{
		auto rect = win32.RECT(0, 0, cx, cy);
		//auto flags = win32.DT_WORDBREAK | win32.DT_EDITCONTROL;
		auto flags = win32.DT_CENTER|win32.DT_VCENTER|win32.DT_SINGLELINE;
		win32.DrawTextEx(hdc, cast(char*)lData, wData, &rect, flags, null);
		return win32.TRUE;
	}
}


class Label : widgets.Label
{
	mixin forward_ctor;
	override void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.FillRect(hdc, &rect, style.appWorkspace);
	}
}


class Dialog : widgets.Dialog
{
	mixin forward_ctor;
	override void paint(win32.HDC hdc)
	{
		auto pos = this.position_abs();
		auto rect = win32.RECT(pos.x, pos.y, pos.x + this.width, pos.y + this.height);

		win32.FillRect(hdc, &rect, style.buttonFace);

		win32.DrawEdge(hdc, &rect, win32.EDGE_RAISED, win32.BF_RECT);
	}
}

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


class IoManager : ui.io!(node_paint_interface).EventManager!(BaseNode)
{
	this (typeof(super.window) window)
	{
		super(window);
	}
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
		foreach_reverse(ref node; this.root)
			node.paint(buffer_dc);
		win32.BitBlt(hdc, 0, 0, rect.right, rect.bottom, buffer_dc, 0, 0, win32.SRCCOPY);
		win32.SelectObject(buffer_dc, old_bitmap);
		win32.DeleteObject(bitmap);
		win32.DeleteDC(buffer_dc);
	}
}

alias sys.WindowGDI!(IoManager) SysWindow;
