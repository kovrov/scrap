struct Point
{
	short x, y;
	const Point opAdd(const ref Point other) { return Point(x +  other.x, y +  other.y); }
	const Point opSub(const ref Point other) { return Point(x -  other.x, y -  other.y); }
	void opAddAssign(const ref Point other)               { x += other.x; y += other.y; }
	void opSubAssign(const ref Point other)               { x -= other.x; y -= other.y; }
}
struct Size { ushort width, height; }

struct Rect
{
	//union
	//{
		Point position;//origin;
	//	struct{ short x, y; }
	//}
	//union
	//{
		Size size;
	//	struct{ ushort width, height; }
	//}

	bool contains(const ref Point point)
	{
		return position.x <= point.x && position.y <= point.y &&
				point.x <= position.x + size.width && point.y <= position.y + size.height;
	}
}


import tree;

class TargetNode
{
	union
	{
		Rect rect;
		struct
		{
			short x, y;
			ushort width, height;
		}
		static assert (Rect.sizeof == short.sizeof*2 + ushort.sizeof*2);
	}
	string name;
	mixin tree.Node;
	mixin tree.setParent;
	mixin tree.opApplyReverse;

	this(string name, typeof(this) parent=null)
	{
		if (parent)
			this.setParent(parent);
		this.name = name;
	}
	Point position_abs()
	{
		Point abs_pos = this.rect.position;
		auto parent = this.parent;
		while (parent)
		{
			abs_pos += parent.rect.position;
			parent = parent.parent;
		}
		return abs_pos;
	}
}


TargetNode findControl(TargetNode root, const ref Point point)
{
	TargetNode best_match;
	int indent = 0;
	Point parent_abs_pos;
	auto node = root;
	while (node !is null)
	{
		if (node.child !is null)  // the node is an internal (inner) node
		{
			if (node.rect.contains(point - parent_abs_pos))
			{
				// save so far best matched target
				best_match = node;
			}
			parent_abs_pos += node.rect.position;
			indent++;
			node = node.child;
		}
		else
		{
			if (node.rect.contains(point - parent_abs_pos))
			{
				// first matched terminal node (leaf) is what we need
				return node;
			}

			if (node.next !is null)  // the node is a leaf
			{
				node = node.next;
				continue;
			}
			else  // the node is a last leaf
			{
				assert (node is node.parent.lastChild);
				if (best_match is node.parent)
				{
					// found best match
					return best_match;
				}
				auto parent = node.parent;
				node = null;
				while (parent !is null)
				{
					indent--;
					parent_abs_pos -= parent.rect.position;
					if (parent.next)
					{
						node = parent.next;
						break;
					}
					parent = parent.parent;
				}
			}
		}
	}
	return best_match;
}


class Window : TargetNode
{
	this(string name, TargetNode parent) { super(name, parent); }
}

class Group : TargetNode
{
	this(string name, TargetNode parent) { super(name, parent); }
}

class Radio : TargetNode
{
	this(string name, TargetNode parent) { super(name, parent); }
}

class Button : TargetNode
{
	this(string name, TargetNode parent) { super(name, parent); }
}

class Label : TargetNode
{
	this(string name, TargetNode parent) { super(name, parent); }
}

class Dialog : TargetNode
{
	this(string name, TargetNode parent) { super(name, parent); }
}



pragma(lib, "win32.lib");
static import win32 = win32.windows;
import std.stdio;


// TEST

TargetNode genTestData()
{
	auto root = new TargetNode("root");
	root.rect.size = Size(640,480);
	  auto dlg = new Dialog("dlg", root);
	  dlg.rect = Rect(Point(200,200),Size(400,200));  // [200,200-600,400]
	    auto b2 = new Button("b2", dlg);
	    b2.rect = Rect(Point(10,10),Size(48,18));     // [210,210-228,258]
	    auto b3 = new Button("b3", dlg);
	    b3.rect = Rect(Point(10,40),Size(50,20));     // [210,240-230,290]
	    auto l2 = new Label("l2", dlg);
	    l2.rect = Rect(Point(10,70),Size(50,20));     // [210,270-230,320]
	  auto wnd = new Window("wnd", root);
	  wnd.rect = Rect(Point(100,100),Size(400,200));  // [100,100-500,300]
	    auto b1 = new Button("b1", wnd);
	    b1.rect = Rect(Point(10,170),Size(30,20));    // [110,270-130,300]
	    auto l1 = new Label("l1", wnd);
	    l1.rect = Rect(Point(50,170),Size(30,20));    // [150,440-170,470]
	    auto grp = new Group("grp", wnd);
	    grp.rect = Rect(Point(10,10),Size(290,150));  // [110,110-400,260]
	      auto r1 = new Radio("r1", grp);
	      r1.rect = Rect(Point(10,10),Size(30,10));   // [120,120-130,170]
	      auto r2 = new Radio("r2", grp);
	      r2.rect = Rect(Point(10,30),Size(30,10));   // [120,140-130,190]
	return root;
}

TargetNode root;
TargetNode tracked;

extern (Windows)
win32.LRESULT WndProc(win32.HWND hWnd, win32.UINT message, win32.WPARAM wParam, win32.LPARAM lParam)
{
	switch (message)
	{
	case win32.WM_PAINT:  // http://msdn.microsoft.com/library/ms534901
		win32.PAINTSTRUCT ps;
		win32.HDC hdc = win32.BeginPaint(hWnd, &ps);
		// http://msdn.microsoft.com/en-us/library/ms969905.aspx
		win32.HDC buffer_dc = win32.CreateCompatibleDC(hdc);
		win32.HBITMAP bitmap = win32.CreateCompatibleBitmap(hdc, ps.rcPaint.right, ps.rcPaint.bottom);
		win32.HBITMAP old_bitmap = win32.SelectObject(buffer_dc, bitmap);

		auto original = win32.GetCurrentObject(buffer_dc, win32.OBJ_BRUSH);
		foreach_reverse(ref node; root)
		{
			if (node is tracked)
				win32.SelectObject(buffer_dc, win32.GetStockObject(win32.GRAY_BRUSH));

			Point pos = node.position_abs();
			win32.Rectangle(buffer_dc,
					pos.x, pos.y,
					pos.x+node.rect.size.width+1, pos.y+node.rect.size.height+1);

			if (node is tracked)
				win32.SelectObject(buffer_dc, original);
		}

		win32.BitBlt(hdc, 0, 0, ps.rcPaint.right, ps.rcPaint.bottom, buffer_dc, 0, 0, win32.SRCCOPY);
		win32.SelectObject(buffer_dc, old_bitmap);
		win32.DeleteObject(bitmap);
		win32.DeleteDC(buffer_dc);
		win32.EndPaint(hWnd, &ps);
		break;
	case win32.WM_MOUSEMOVE:  // http://msdn.microsoft.com/library/ms645616
		auto target = findControl(root, Point(win32.LOWORD(lParam), win32.HIWORD(lParam)));
		if (tracked !is target)
		{
			tracked = target;
			win32.InvalidateRect(hWnd, null, false);
		}
		break;
	case win32.WM_DESTROY:
		win32.PostQuitMessage(0);
		break;
	default:
		return win32.DefWindowProc(hWnd, message, wParam, lParam);
	}
	return 0;
}

void main()
{
	//TEST
	root = genTestData();

	// init instance
	win32.WNDCLASSEX wcex;
	wcex.style			= win32.CS_HREDRAW | win32.CS_VREDRAW;
	wcex.lpfnWndProc	= &WndProc;
	wcex.hInstance		= win32.GetModuleHandle(null);
	wcex.hCursor        = win32.LoadCursor(null,  win32.IDC_ARROW);
	wcex.lpszClassName	= "test_window";
	if (!win32.RegisterClassEx(&wcex))
		throw new Exception("RegisterClass failed");
	win32.HWND hWnd = win32.CreateWindow(wcex.lpszClassName, "test",
				win32.WS_OVERLAPPEDWINDOW, win32.CW_USEDEFAULT,
				0, win32.CW_USEDEFAULT, 0, null, null, wcex.hInstance, null);
	if (!hWnd)
		throw new Exception("CreateWindow failed");

	win32.ShowWindow(hWnd, win32.SW_SHOWNORMAL);
	win32.UpdateWindow(hWnd);

	// Main message loop:
	win32.MSG msg;
	while (win32.GetMessage(&msg, null, 0, 0))
	{
		win32.DispatchMessage(&msg);
	}
}
