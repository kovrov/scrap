
import std.bitmanip;
debug import std.string;

class Widget
{
	short x, y;
	short width, height;
	mixin(bitfields!(
		bool, "ContentsVisible", 1, // BaseRegion, StaticRectangle
		bool, "BorderVisible",   1, // BaseRegion, StaticRectangle, color picker?
		bool, "Link",            1, // button?
		bool, "DefaultOK",       1, // Button; meant to be used by BaseRegion
		bool, "DefaultBack",     1, // Button; meant to be used by BaseRegion
		bool, "Disabled",        1, // Button, ScrollBar, ListWindow, TextEntry, (any?)
		bool, "DontCutoutBase",  1, // CutoutRegion, (any?); rationale?
		bool, "CallOnCreate",    1, // any?
		bool, "CallOnDelete",    1, // any?
		bool, "Background",      1, // Button, ToggleButton
		bool, "Hidden",          1, // (any?); rationale?
		bool, "Bitmap",          1, // unused
		uint, "",  4));  // padding to 16-bit
	uint[2] drawstyle;

	this(short x, short y, short w, short h)
	{
		this.x = x;
		this.y = y;
		this.width = w;
		this.height = h;
	}

	void draw()  // feStaticRectangleDraw
	{
	}

	debug override string toString()
	{
		return format("%s [%s,%s, %s,%s]", this.classinfo.name, x,y,width,height);
	}
}

class BaseRegion: Widget
{
	bool popup;
	bool modal;
	//bool alwaysOnTop;
	bool draggable;
	this(short x, short y, short w, short h) { super(x,y,w,h); }
}

class NullWidget : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
}

class UserRegion : Widget
{
	string draw_callback_name;
	this(short x, short y, short w, short h, string draw_callback_name)
	{
		super(x,y,w,h);
		this.draw_callback_name = draw_callback_name;
	}

	override void draw()  // feUserRegionDraw
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

	override void draw()  // feStaticTextDraw
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

	override void draw()  // uicButtonDraw
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

	override void draw()  // uicButtonDraw
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

	override void draw()  // uicToggleDraw
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
		/* vertical scrollbars has complex structure see uicChildScrollBarAlloc */
	}

	debug override string toString()
	{
		return super.toString() ~ " callback:<" ~ callback_name ~ ">";
	}
}

class TextEntry : Widget
{
	this(short x, short y, short w, short h) { super(x,y,w,h); }
	override void draw()  // uicTextEntryDraw
	{
	}
}

/*
class StatusBar : Widget
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
*/

class MenuItem : Widget
{
	string callback_name;

	this(short x, short y, short w, short h, string callback_name)
	{
		super(x,y,w,h);
		this.callback_name = callback_name;
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

	override void draw()  // uicRadioButtonDraw
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
	override void draw() // dont have a draw fn?
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

	override void draw()  // ferDrawDecorative
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
}

class ListWindow : Widget
{
	string callback_name;
	ScrollBar scrollbar;  // list window have to have a scrollbar ...

	this(short x, short y, short w, short h, string callback_name)
	{
		super(x,y,w,h);
		this.callback_name = callback_name;
	}

	override void draw()  // uicListWindowDraw
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

	override void draw()  // uicBitmapButtonDraw
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

	override void draw()  // uicHorizSliderDraw
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

	override void draw()  // uicVertSliderDraw
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

	override void draw()  // uicButtonDraw
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

	override void draw()  // ferDrawOpaqueDecorative
	{
	}

	debug override string toString()
	{
		return super.toString() ~ " img:<" ~ img_name ~ ">";
	}
}
