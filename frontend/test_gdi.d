pragma(lib, "win32.lib");
static import win32 = win32.windows;

static import sys;
static import ui;
static import widget;
static import gdi;

alias widget.Widget!(gdi.paint_simple_window)         Widget;
alias widget.Window!(gdi.paint_simple_window, Widget) Window;
alias widget.Dialog!(gdi.paint_simple_window, Widget) Dialog;
alias widget.Group !(gdi.paint_simple_window, Widget) Group;
alias widget.Button!(gdi.paint_simple_window, Widget) Button;
alias widget.Radio !(gdi.paint_simple_window, Widget) Radio;
alias widget.Label !(gdi.paint_simple_window, Widget) Label;

static import generic;
alias generic.Rect!(short, ushort) Rect;

Widget genTestData()
{
	auto root = new Widget("root");
	root.rect.size = sys.Size(640,480);
	  auto dlg = new Dialog("dlg", root);
	  dlg.rect = Rect(sys.Point(200,200),sys.Size(400,200));  // [200,200-600,400]
	    auto b2 = new Button("b2", dlg);
	    b2.rect = Rect(sys.Point(10,10),sys.Size(48,18));     // [210,210-228,258]
	    auto b3 = new Button("b3", dlg);
	    b3.rect = Rect(sys.Point(10,40),sys.Size(50,20));     // [210,240-230,290]
	    auto l2 = new Label("l2", dlg);
	    l2.rect = Rect(sys.Point(10,70),sys.Size(50,20));     // [210,270-230,320]
	  auto wnd = new Window("wnd", root);
	  wnd.rect = Rect(sys.Point(100,100),sys.Size(400,200));  // [100,100-500,300]
	    auto b1 = new Button("b1", wnd);
	    b1.rect = Rect(sys.Point(10,170),sys.Size(30,20));    // [110,270-130,300]
	    auto l1 = new Label("l1", wnd);
	    l1.rect = Rect(sys.Point(50,170),sys.Size(30,20));    // [150,440-170,470]
	    auto grp = new Group("grp", wnd);
	    grp.rect = Rect(sys.Point(10,10),sys.Size(290,150));  // [110,110-400,260]
	      auto r1 = new Radio("r1", grp);
	      r1.rect = Rect(sys.Point(10,10),sys.Size(30,10));   // [120,120-130,170]
	      auto r2 = new Radio("r2", grp);
	      r2.rect = Rect(sys.Point(10,30),sys.Size(30,10));   // [120,140-130,190]
	return root;
}


alias ui.IoManager!(gdi.paint_events) IoManagerGDI;
alias sys.Window!(IoManagerGDI) WindowGDI;


void main()
{
	auto window = WindowGDI("test", sys.Size(640,480), WindowGDI.FLAG.hidden);
	ui.TargetNode main_ui = genTestData();  // load main UI
//	window.io.bind(main_ui);
//	window.paint_handler = delegate(win32.HDC hdc)
//		{
//			foreach_reverse(ref node; root)
//				(cast(Widget)node).paint(hdc);
//		};
	window.visible(true);

	// Main message loop:
	sys.messageLoop();
}
