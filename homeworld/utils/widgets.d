
import std.bitmanip;
debug import std.string;

class Widget
{
	short x, y;
	short width, height;
	mixin(bitfields!(
		bool, "Link",            1,
		bool, "Function",        1,
		bool, "Modal",           1,
		bool, "Popup",           1,
		bool, "CallOnCreate",    1,
		bool, "ContentsVisible", 1,
		bool, "DefaultOK",       1,
		bool, "DefaultBack",     1,
		bool, "AlwaysOnTop",     1,
		bool, "Draggable",       1,
		bool, "BorderVisible",   1,
		bool, "Disabled",        1,
		bool, "DontCutoutBase",  1,
		bool, "CallOnDelete",    1,
		bool, "Background",      1,
		bool, "Hidden",          1));
		//bool, "Bitmap",          1,
		//uint, "",       15));  // 32-bit
	uint[2] drawstyle;

	this(short x, short y, short w, short h)
	{
		this.x = x;
		this.y = y;
		this.width = w;
		this.height = h;
	}

	abstract void draw();

	debug override string toString()
	{
		return format("%s [%s,%s, %s,%s]", this.classinfo.name, x,y,width,height);
	}
}

class NullWidget : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	override void draw()
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

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " draw_callback:<" ~ draw_callback_name ~ ">";
	}
}

class StaticText : Widget
{
	string text;
	string font_name;
	this(short x, short y, short w, short h, string text, string font_name)
	{
		super(x,y,w,h);
		this.text = text;
		this.font_name = font_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " font:<" ~ font_name ~ "> text<" ~ text ~ ">";
	}
}

class Button : Widget
{
	string target_name;

	this(short x, short y, short w, short h, string target_name)
	{
		super(x,y,w,h);
		this.target_name = target_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " target:<" ~ target_name ~ ">";
	}
}

class CheckBox : Widget
{
	string callback_name;

	this(short x, short y, short w, short h, string callback_name)
	{
		super(x,y,w,h);
		this.callback_name = callback_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " callback:<" ~ callback_name ~ ">";
	}
}

class ToggleButton : Widget
{
	string callback_name;

	this(short x, short y, short w, short h, string callback_name)
	{
		super(x,y,w,h);
		this.callback_name = callback_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " callback:<" ~ callback_name ~ ">";
	}
}

class ScrollBar : Widget
{
	string callback_name;

	this(short x, short y, short w, short h, string callback_name)
	{
		super(x,y,w,h);
		this.callback_name = callback_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " callback:<" ~ callback_name ~ ">";
	}
}

class StatusBar : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	override void draw()
	{
	}
}

class TextEntry : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	override void draw()
	{
	}
}

class ListViewExpandButton : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	override void draw()
	{
	}
}

class TitleBar : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	override void draw()
	{
	}
}

class MenuItem : Widget
{
	string callback_name;

	this(short x, short y, short w, short h, string callback_name)
	{
		super(x,y,w,h);
		this.callback_name = callback_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " callback:<" ~ callback_name ~ ">";
	}
}

class RadioButton : Widget
{
	string callback_name;

	this(short x, short y, short w, short h, string callback_name)
	{
		super(x,y,w,h);
		this.callback_name = callback_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " callback:<" ~ callback_name ~ ">";
	}
}

class CutoutRegion : Widget  // FIXME: find out what CutoutRegion's are for
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	override void draw()
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

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " img:<" ~ img_name ~ ">";
	}
}

class Divider : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	override void draw()
	{
	}
}

class ListWindow : Widget
{
	string callback_name;

	this(short x, short y, short w, short h, string callback_name)
	{
		super(x,y,w,h);
		this.callback_name = callback_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " callback:<" ~ callback_name ~ ">";
	}
}

class BitmapButton : Widget
{
	string callback_name;

	this(short x, short y, short w, short h, string callback_name)
	{
		super(x,y,w,h);
		this.callback_name = callback_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " callback:<" ~ callback_name ~ ">";
	}
}

class HorizSlider : Widget
{
	string callback_name;

	this(short x, short y, short w, short h, string callback_name)
	{
		super(x,y,w,h);
		this.callback_name = callback_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " callback:<" ~ callback_name ~ ">";
	}
}

class VertSlider : Widget
{
	string callback_name;

	this(short x, short y, short w, short h, string callback_name)
	{
		super(x,y,w,h);
		this.callback_name = callback_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " callback:<" ~ callback_name ~ ">";
	}
}

class DragButton : Widget
{
	string function_name;

	this(short x, short y, short w, short h, string function_name)
	{
		super(x,y,w,h);
		this.function_name = function_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " callback:<" ~ function_name ~ ">";
	}
}

class OpaqueDecorativeRegion : Widget
{
	string img_name;

	this(short x, short y, short w, short h, string img_name)
	{
		super(x,y,w,h);
		this.img_name = img_name;
	}

	override void draw()
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " img:<" ~ img_name ~ ">";
	}
}
