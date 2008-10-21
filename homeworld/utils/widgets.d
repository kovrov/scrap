
class Widget
{
	short x, y;
	short width, height;
	uint flags; // FAF
	string name;

	this(short x, short y, short w, short h)
	{
		this.x = x;
		this.y = y;
		this.width = w;
		this.height = h;
	}

	abstract void draw();
}

class NullWidget : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class UserRegion : Widget
{
	string draw_callback_name;
	this(short x, short y, short w, short h, string draw_callback_name)
	{
		super(x,y,w,h);
		this.draw_callback_name = draw_callback_name;
	}

	void draw()
	{
	}
}

class StaticText : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class Button : Widget
{
	string target_name;

	this(short x, short y, short w, short h, string target)
	{
		super(x,y,w,h);
		this.target_name = target_name;
	}

	void draw()
	{
	}
}

class CheckBox : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class ToggleButton : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class ScrollBar : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class StatusBar : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class TextEntry : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class ListViewExpandButton : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class TitleBar : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class MenuItem : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class RadioButton : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class CutoutRegion : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class DecorativeRegion : Widget
{
	string img_name;

	this(short x, short y, short w, short h, string img_name)
	{
		super(x,y,w,h);
		this.img_name = img_name;
	}
	void draw()
	{
	}
}

class Divider : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class ListWindow : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class BitmapButton : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class HorizSlider : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class VertSlider : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class DragButton : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}

class OpaqueDecorativeRegion : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	void draw()
	{
	}
}
