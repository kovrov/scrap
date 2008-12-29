
static import sys;
static import gdi;

static import generic;
alias generic.Rect!(short, ushort) Rect;

gdi.Widget genTestData()
{
	auto root = new gdi.Widget("root");
	root.rect.size = sys.Size(640,480);
	  auto dlg = new gdi.Dialog("dlg", root);
	  dlg.rect = Rect(sys.Point(200,200),sys.Size(400,200));
	    auto b2 = new gdi.Button("b2", dlg);
	    b2.rect = Rect(sys.Point(10,10),sys.Size(48,22));
	    auto b3 = new gdi.Button("b3", dlg);
	    b3.rect = Rect(sys.Point(10,40),sys.Size(50,22));
	    auto l2 = new gdi.Label("l2", dlg);
	    l2.rect = Rect(sys.Point(10,70),sys.Size(50,20));
	  auto wnd = new gdi.Window("wnd", root);
	  wnd.rect = Rect(sys.Point(100,100),sys.Size(400,200));
	    auto b1 = new gdi.Button("b1", wnd);
	    b1.rect = Rect(sys.Point(10,170),sys.Size(30,22));
	    auto l1 = new gdi.Label("l1", wnd);
	    l1.rect = Rect(sys.Point(50,170),sys.Size(30,20));
	    auto grp = new gdi.Group("grp", wnd);
	    grp.rect = Rect(sys.Point(10,10),sys.Size(290,150));
	      auto r1 = new gdi.Radio("r1", grp);
	      r1.rect = Rect(sys.Point(10,10),sys.Size(30,10));
	      auto r2 = new gdi.Radio("r2", grp);
	      r2.rect = Rect(sys.Point(10,30),sys.Size(30,10));
	return root;
}


void main()
{
	auto window = gdi.SysWindow("test", sys.Size(640,480), sys.Window.FLAG.hidden|sys.Window.FLAG.resizable);
	auto main_ui = genTestData();  // load main UI
	window.io.root = main_ui;  //bind
	window.visible(true);
	// Main message loop:
	sys.messageLoop();
}
