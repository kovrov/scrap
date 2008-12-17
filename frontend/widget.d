static import ui;
static import sys;

class Widget(alias PAINT=null) : ui.TargetNode
{
	this(string name, ui.TargetNode parent=null)
	{
		super(name, parent);
		this.mouseEventMask = sys.MOUSE.MOVE;
	}

	static if (typeid(typeof(PAINT)) !is typeid(typeof(null)))
		mixin PAINT;

	//bool tracked;
	override void onMouse(ref sys.MouseEvent ev)
	{
	//	this.tracked = true;
	//	app.window.redraw();
	}
}


template parent_ctor() { this(string name, ui.TargetNode parent) { super(name, parent); }}


class Window(alias PAINT) : Widget!()
{
	mixin parent_ctor;
	mixin PAINT;
}

class Group(alias PAINT) : Widget!()
{
	mixin parent_ctor;
	mixin PAINT;
}

class Radio(alias PAINT) : Widget!()
{
	mixin parent_ctor;
	mixin PAINT;
}

class Button(alias PAINT) : Widget!()
{
	mixin parent_ctor;
	mixin PAINT;
}

class Label(alias PAINT) : Widget!()
{
	mixin parent_ctor;
	mixin PAINT;
}

class Dialog(alias PAINT) : Widget!()
{
	mixin parent_ctor;
	mixin PAINT;
}
