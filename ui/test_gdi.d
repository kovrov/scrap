pragma(lib, "win32.lib");
static import win32 = win32.windows;
static import generic;
alias generic.Point!(short) Point;
alias generic.Size!(ushort) Size;
alias generic.Rect!(short, ushort) Rect;
import std.stdio;
import sys;


class Window : event.TargetNode
{
	this(string name, event.TargetNode parent) { super(name, parent); }
}

class Group : event.TargetNode
{
	this(string name, event.TargetNode parent) { super(name, parent); }
}

class Radio : event.TargetNode
{
	this(string name, event.TargetNode parent) { super(name, parent); }
}

class Button : event.TargetNode
{
	this(string name, event.TargetNode parent) { super(name, parent); }
}

class Label : event.TargetNode
{
	this(string name, event.TargetNode parent) { super(name, parent); }
}

class Dialog : event.TargetNode
{
	this(string name, event.TargetNode parent) { super(name, parent); }
}

event.TargetNode genTestData()
{
	auto root = new event.TargetNode("root");
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


struct App
{
	struct 
	{
		Size winsize = Size(640,480);
		void loadSettings() {}
	}
	string name = "test";
	sys.Window window;
	void* render;
	void* simulation;
}


static import event;
void main()
{
	event.TargetNode tracked;
	event.TargetNode root = genTestData();
	App app;
	app.loadSettings();
	app.window = sys.Window(app.name, app.winsize, sys.Window.FLAG.hidden);
	app.window.event_mgr.register(
		delegate (ref event.MouseEvent ev)
		{
			auto target = event.findControl(root, ev.pos);
			if (tracked !is target)
			{
				tracked = target;
				app.window.redraw();
			}
		});
	app.window.paint_handler = delegate(win32.HDC hdc)
	{
		auto original = win32.GetCurrentObject(hdc, win32.OBJ_BRUSH);
		foreach_reverse(ref node; root)
		{
			if (node is tracked)
				win32.SelectObject(hdc, win32.GetStockObject(win32.GRAY_BRUSH));

			Point pos = node.position_abs();
			win32.Rectangle(hdc,
					pos.x, pos.y,
					pos.x+node.rect.size.width, pos.y+node.rect.size.height);

			if (node is tracked)
				win32.SelectObject(hdc, original);
		}
	};
	app.window.visible(true);

	// Main message loop:
	win32.MSG msg;
	while (win32.GetMessage(&msg, null, 0, 0))
	{
		win32.DispatchMessage(&msg);
	}
}
