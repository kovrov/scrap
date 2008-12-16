static import sys;
static import ui;


class Window : ui.TargetNode
{
	this(string name, ui.TargetNode parent) { super(name, parent); }
}

class Group : ui.TargetNode
{
	this(string name, ui.TargetNode parent) { super(name, parent); }
}

class Radio : ui.TargetNode
{
	this(string name, ui.TargetNode parent) { super(name, parent); }
}

class Button : ui.TargetNode
{
	this(string name, ui.TargetNode parent) { super(name, parent); }
}

class Label : ui.TargetNode
{
	this(string name, ui.TargetNode parent) { super(name, parent); }
}

class Dialog : ui.TargetNode
{
	this(string name, ui.TargetNode parent) { super(name, parent); }
}

ui.TargetNode genTestData()
{
	auto root = new ui.TargetNode("root");
	root.rect.size = ui.Size(640,480);
	  auto dlg = new Dialog("dlg", root);
	  dlg.rect = ui.Rect(ui.Point(200,200),ui.Size(400,200));  // [200,200-600,400]
	    auto b2 = new Button("b2", dlg);
	    b2.rect = ui.Rect(ui.Point(10,10),ui.Size(48,18));     // [210,210-228,258]
	    auto b3 = new Button("b3", dlg);
	    b3.rect = ui.Rect(ui.Point(10,40),ui.Size(50,20));     // [210,240-230,290]
	    auto l2 = new Label("l2", dlg);
	    l2.rect = ui.Rect(ui.Point(10,70),ui.Size(50,20));     // [210,270-230,320]
	  auto wnd = new Window("wnd", root);
	  wnd.rect = ui.Rect(ui.Point(100,100),ui.Size(400,200));  // [100,100-500,300]
	    auto b1 = new Button("b1", wnd);
	    b1.rect = ui.Rect(ui.Point(10,170),ui.Size(30,20));    // [110,270-130,300]
	    auto l1 = new Label("l1", wnd);
	    l1.rect = ui.Rect(ui.Point(50,170),ui.Size(30,20));    // [150,440-170,470]
	    auto grp = new Group("grp", wnd);
	    grp.rect = ui.Rect(ui.Point(10,10),ui.Size(290,150));  // [110,110-400,260]
	      auto r1 = new Radio("r1", grp);
	      r1.rect = ui.Rect(ui.Point(10,10),ui.Size(30,10));   // [120,120-130,170]
	      auto r2 = new Radio("r2", grp);
	      r2.rect = ui.Rect(ui.Point(10,30),ui.Size(30,10));   // [120,140-130,190]
	return root;
}


struct App
{
	struct 
	{
		ui.Size winsize = ui.Size(640,480);
		void loadSettings() {}
	}
	string name = "test";
	sys.Window window;
	void* render;
	void* simulation;
}


static import win32 = win32.windows;

void main()
{
/*
	auto window = sys.Window();
	ui.EventManager ui_event_mgr;
	void delegate(gdi grapgics) ui_draw;


	void* ui; // something could be binded to input/output

	auto mouse_handler = delegate (ref ui.MouseEvent ev)
		{
			auto target = ui.findControl(ui.root, ev.pos);
			if (target !is null && target.onMouse !is null)
				target.onMouse(ev);
		}

	window.event_mgr = ui_event_mgr;

	void* simulation;  // something could be binded to input/output
*/
	ui.TargetNode tracked;
	ui.TargetNode root = genTestData();
	App app;
	app.loadSettings();
	app.window = sys.Window(app.name, app.winsize, sys.Window.FLAG.hidden);
	app.window.event_mgr.register(
		delegate (ref ui.MouseEvent ev)
		{
			auto target = ui.findControl(root, ev.pos);
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

			auto pos = node.position_abs();
			win32.Rectangle(hdc,
					pos.x, pos.y,
					pos.x+node.rect.size.width, pos.y+node.rect.size.height);

			if (node is tracked)
				win32.SelectObject(hdc, original);
		}
	};
	app.window.visible(true);

	// Main message loop:
	sys.messageLoop();
}
