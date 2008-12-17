static import ui;
static import sys;

class Widget(alias PAINT) : ui.TargetNode
{
	this(string name, ui.TargetNode parent=null)
	{
		super(name, parent);
		this.mouseEventMask = sys.MOUSE.MOVE;
	}

	mixin PAINT;

	//bool tracked;
	override void onMouse(ref sys.MouseEvent ev)
	{
	//	this.tracked = true;
	//	app.window.redraw();
	}
}


template parent_ctor() { this(string name, ui.TargetNode parent) { super(name, parent); }}


class Window(alias PAINT, BASE) : BASE
{
	mixin parent_ctor;
	mixin PAINT;
}

class Group(alias PAINT, BASE) : BASE
{
	mixin parent_ctor;
	mixin PAINT;
}

class Radio(alias PAINT, BASE) : BASE
{
	mixin parent_ctor;
	mixin PAINT;
}

class Button(alias PAINT, BASE) : BASE
{
	mixin parent_ctor;
	mixin PAINT;
}

class Label(alias PAINT, BASE) : BASE
{
	mixin parent_ctor;
	mixin PAINT;
}

class Dialog(alias PAINT, BASE) : BASE
{
	mixin parent_ctor;
	mixin PAINT;
}
