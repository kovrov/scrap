static import sys;
static import gdi;

gdi.Widget genTestData()
{

	auto root = new gdi.Widget("root"); with (root) { width=640; height=480; }

	  auto dlg = new gdi.Window("dlg", root);
	  with (dlg) { x=200; y=200; width=400; height=200; nested=false; }
	    with (new gdi.Button("b2", dlg)) { x=10; y=10; width=48; height=22; }
	    with (new gdi.Button("b3", dlg)) { x=10; y=40; width=50; height=22; }
	    with (new gdi.Label("label one", dlg)) { x=10; y=70; width=50; height=20; }

	  auto wnd = new gdi.Window("wnd", root);
	  with (wnd) { x=100; y=100; width=400; height=200; nested=false; }
	    with (new gdi.Button("b1", wnd)) { x=10; y=170; width=30; height=22; }
	    with (new gdi.Label("label two", wnd)) { x=50; y=170; width=50; height=20; }
	    auto grp = new gdi.Group("grp", wnd);
	    with (grp) { x=10; y=10; width=290; height=150; }
	      with (new gdi.Radio("r1", grp)) { x=10; y=10; width=30; height=10; }
	      with (new gdi.Radio("r2", grp)) { x=10; y=30; width=30; height=10; }

	  // test
	  with (new gdi.Button("b4", root)) { x=620; y=460; width=48; height=22; nested=false; }
	  with (new gdi.Button("b5", root)) { x=610; y=470; width=48; height=22; nested=false; }

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
