static import ui;

class Widget(alias PAINT, BASE) : BASE  //ui.TargetNode!(paint_interface)
{
	this(string name, BASE parent=null)
	{
		super(name, parent);
		this.mouseEventMask = ui.MOUSE.MOVE;
	}

	mixin PAINT;

	//bool tracked;
	override void onMouse(ref ui.MouseEvent ev)
	{
	//	this.tracked = true;
	//	app.window.redraw();
	}
}


template parent_ctor(BASE) { this(string name, BASE parent) { super(name, parent); }}


class Window(alias PAINT, ANCESTOR, BASE) : ANCESTOR
{
	mixin parent_ctor!(BASE);
	mixin PAINT;
}

class Group(alias PAINT, ANCESTOR, BASE) : ANCESTOR
{
	mixin parent_ctor!(BASE);
	mixin PAINT;
}

class Radio(alias PAINT, ANCESTOR, BASE) : ANCESTOR
{
	mixin parent_ctor!(BASE);
	mixin PAINT;
}

class Button(alias PAINT, ANCESTOR, BASE) : ANCESTOR
{
	mixin parent_ctor!(BASE);
	mixin PAINT;
}

class Label(alias PAINT, ANCESTOR, BASE) : ANCESTOR
{
	mixin parent_ctor!(BASE);
	mixin PAINT;
}

class Dialog(alias PAINT, ANCESTOR, BASE) : ANCESTOR
{
	mixin parent_ctor!(BASE);
	mixin PAINT;
}
