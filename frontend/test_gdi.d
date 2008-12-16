static import sys;
static import gdi;
static import ui;
static import win32 = win32.windows;
pragma(lib, "win32.lib");

class GdiWindow : ui.TargetNode
{
	bool tracked;
	this(string name, ui.TargetNode parent)
	{
		super(name, parent);
		this.mouseEventMask = ui.MOUSE.MOVE;
	}
	void paint(win32.HDC hdc)
	{
		auto pos = node.position_abs();
		win32.Rectangle(hdc,
				pos.x, pos.y,
				pos.x+node.rect.size.width, pos.y+node.rect.size.height);
	}
	override void onMouse(ref ui.MouseEvent ev)
	{
		//this.tracked = true;
		//app.window.redraw();
	}
}


class Window : GdiWindow
{
	this(string name, ui.TargetNode parent) { super(name, parent); }
}

class Group : GdiWindow
{
	this(string name, ui.TargetNode parent) { super(name, parent); }
}

class Radio : GdiWindow
{
	this(string name, ui.TargetNode parent) { super(name, parent); }
}

class Button : GdiWindow
{
	this(string name, ui.TargetNode parent) { super(name, parent); }
}

class Label : GdiWindow
{
	this(string name, ui.TargetNode parent) { super(name, parent); }
}

class Dialog : GdiWindow
{
	this(string name, ui.TargetNode parent) { super(name, parent); }
}

ui.TargetNode genTestData()
{
	auto root = new GdiWindow("root");
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


void main()
{
	auto window = sys.Window!(ui.IoManager)("test", ui.Size(640,480), sys.Window.FLAG.hidden);
	ui.TargetNode main_ui = genTestData();  // load main UI
	window.io.bind(main_ui);
	app.window.paint_handler = delegate(win32.HDC hdc)
		{
			foreach_reverse(ref node; root)
				(cast(GdiWindow)node).paint(hdc);
		};
	app.window.visible(true);

	// Main message loop:
	sys.messageLoop();
}
