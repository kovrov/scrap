/+

a GUI layer...

* A list of widgets (buttons, check boxes, etc).
* Position and state variables.
* Logic to keep the widgets coordinated, relying on
  the state and position variables to tell the widgets
  where they are supposed to be.

+/

import std.file;
import std.stdio;
import std.string;

import widgets;


struct Link
{
	string name;    //optional name of this link
	string target;  //name of screen to link to
	//FL flags;       //flags controlling behaviour of link
}

struct Screen
{
	string name;
	Widget[] widgets;
	Link[] links;
	this(string scrname)
	{
		name = scrname;
	}
}



void load(string filename, inout Screen[string] screens)
{
	scope fib = FibFile(filename);

	foreach (ref fibscr; fib.screens)
	{
		Screen screen;

		assert (fibscr.ptr.name_fixup != 0, "screens need a name");
		screen.name = toString(cast(char*)fibscr.ptr.name_fixup + fib.mem_offset);

		screen.links.length = fibscr.links.length;
		foreach (i, ref link; screen.links)
		{
			const fiblink = &fibscr.links[i];

			if (! fiblink.flags & FL.Enabled) continue;

			assert (fiblink.name_fixup != 0);
			link.name = toString(cast(char*)fiblink.name_fixup + fib.mem_offset);

			assert (fiblink.linkToName_fixup !is null);
			link.target = toString(fiblink.linkToName_fixup + fib.mem_offset);
		}

		/*	see if there are any menu items present in the screen so we can
			know if we should reposition the screen for high-rez */
		bool menuItemsPresent = false;
		if (screen.name == "HyperspaceRollCall")
		{
			menuItemsPresent = true;
		}
		else
		{
			foreach (ref atom; fibscr.atoms)
			{
				if (atom.type == FA.MenuItem)
				{
					menuItemsPresent = true;
					break;
				}
			}
		}

		screen.widgets.length = fibscr.atoms.length;
		foreach (i, ref widget; screen.widgets)
		{
			const fibAtom = &fibscr.atoms[i];
			// basic checks...
			assert (fibAtom.width  > fibAtom.x);
			assert (fibAtom.height > fibAtom.y);

			short width = fibAtom.width - fibAtom.x;
			short height = fibAtom.height - fibAtom.y;

			FA atom_type = fibAtom.type;
			if (fibAtom.pData_fixup && !(fibAtom.flags & FAF.Bitmap) && fibAtom.type != FA.RadioButton)
			{
				assert (fibAtom.type == 0);
				atom_type = FA.StaticText;
			}

			switch (atom_type)
			{
			case FA.UserRegion:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.tabstop == 0);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				assert (fibAtom.flags & FAF.Function);
				string draw_callback_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.UserRegion(fibAtom.x, fibAtom.y, width, height, draw_callback_name);
				break;

			case FA.StaticText:
				assert (fibAtom.name_fixup == 0);
				assert (fibAtom.attribs_fixup != 0); // font
				assert (fibAtom.pData_fixup != 0);  // text
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.tabstop == 0);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				string text = toString(cast(char*)fibAtom.pData_fixup + fib.mem_offset);
				string font_name = toString(cast(char*)fibAtom.attribs_fixup + fib.mem_offset);
				widget = new widgets.StaticText(fibAtom.x, fibAtom.y, width, height, text, font_name);
				//fibAtom.hotKeyModifiers
				//fibAtom.hotKey
				//fibAtom.pad2
				break;

			case FA.Button:
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				string target_name;
				if (fibAtom.flags & FAF.Function)
				{
					assert (fibAtom.name_fixup);
					target_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				}
				widget = new widgets.Button(fibAtom.x, fibAtom.y, width, height, target_name);
				//fibAtom.tabstop
				//fibAtom.hotKeyModifiers
				//fibAtom.hotKey
				break;

			case FA.CheckBox:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				assert (fibAtom.flags & FAF.Function);
				string callback_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.CheckBox(fibAtom.x, fibAtom.y, width, height, callback_name);
				//fibAtom.tabstop
				break;

			case FA.ToggleButton:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				assert (fibAtom.flags & FAF.Function);
				string callback_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.ToggleButton(fibAtom.x, fibAtom.y, width, height, callback_name);
				//fibAtom.tabstop
				//fibAtom.hotKeyModifiers
				//fibAtom.hotKey
				break;

			case FA.ScrollBar:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.tabstop == 0);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				assert (fibAtom.flags & FAF.Function);
				string callback_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.ScrollBar(fibAtom.x, fibAtom.y, width, height, callback_name);
				break;

			case FA.TextEntry:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				assert (fibAtom.flags & FAF.Function); // WTF?
				// TODO: font ...
				widget = new widgets.TextEntry(fibAtom.x, fibAtom.y, width, height);
				//fibAtom.tabstop
				break;

			//case FA.ListViewExpandButton:  // unused?
			//	widget = new widgets.ListViewExpandButton(fibAtom.x, fibAtom.y, width, height);
			//	break;

			//case FA.TitleBar:  // unused?
			//	widget = new widgets.TitleBar(fibAtom.x, fibAtom.y, width, height);
			//	break;

			//case FA.StatusBar:  // unused?
			//	widget = new widgets.StatusBar(fibAtom.x, fibAtom.y, width, height);
			//	break;

			case FA.MenuItem:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.tabstop == 0);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				//assert (fibAtom.flags & FAF.Function);
				string callback_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.MenuItem(fibAtom.x, fibAtom.y, width, height, callback_name);
				break;

			case FA.RadioButton:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);
				//HACK: don't fix-up radio button pointers
				assert (fibAtom.flags & FAF.Function);
				string callback_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.RadioButton(fibAtom.x, fibAtom.y, width, height, callback_name);
				//fibAtom.tabstop
				//fibAtom.hotKeyModifiers
				//fibAtom.hotKey
				break;

			case FA.CutoutRegion:  // FIXME: find out what CutoutRegion's are for
				assert (fibAtom.name_fixup == 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.tabstop == 0);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				widget = new widgets.CutoutRegion(fibAtom.x, fibAtom.y, width, height);
				break;

			case FA.DecorativeRegion:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.tabstop == 0);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				string img_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.DecorativeRegion(fibAtom.x, fibAtom.y, width, height, img_name);
				break;

			case FA.Divider:
				assert (fibAtom.name_fixup == 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.tabstop == 0);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				widget = new widgets.Divider(fibAtom.x, fibAtom.y, width, height);
				break;

			case FA.ListWindow:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				assert (fibAtom.flags & FAF.Function);
				string callback_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.ListWindow(fibAtom.x, fibAtom.y,
							width - LW_BarWidth - LW_WindowXBarSpace, height,
							callback_name);
				//fibAtom.tabstop;
				break;

			case FA.BitmapButton:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup != 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.tabstop == 0);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				assert (fibAtom.flags & FAF.Function);
				string callback_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.BitmapButton(fibAtom.x, fibAtom.y, width, height, callback_name);
				break;

			case FA.HorizSlider:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.tabstop == 0);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				assert (fibAtom.flags & FAF.Function);
				string callback_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.HorizSlider(fibAtom.x, fibAtom.y, width, height, callback_name);
				break;

			case FA.VertSlider:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.tabstop == 0);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				assert (fibAtom.flags & FAF.Function);
				string callback_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.VertSlider(fibAtom.x, fibAtom.y, width, height, callback_name);
				break;

			case FA.DragButton:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				assert (fibAtom.flags & FAF.Function);
				string function_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.DragButton(fibAtom.x, fibAtom.y, width, height, function_name);
				//fibAtom.hotKeyModifiers;
				//fibAtom.hotKey;
				//fibAtom.tabstop;
				break;

			case FA.OpaqueDecorativeRegion:
				assert (fibAtom.name_fixup != 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.tabstop == 0);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				string img_name = toString(cast(char*)fibAtom.name_fixup + fib.mem_offset);
				widget = new widgets.OpaqueDecorativeRegion(fibAtom.x, fibAtom.y, width, height, img_name);
				break;

			case 0:
				assert (fibAtom.name_fixup == 0);
				assert (fibAtom.attribs_fixup == 0);
				assert (fibAtom.pData_fixup == 0);
				assert (fibAtom.status == 0xCDCDCDCD);
				assert (fibAtom.tabstop == 0);
				assert (fibAtom.hotKeyModifiers == 0);
				assert (fibAtom.hotKey == [cast(ubyte)0,0,0,0,0]);
				assert (fibAtom.pad2 == [cast(ubyte)0,0xCD]);
				assert (fibAtom.pad == [0xCDCDCDCD,0xCDCDCDCD]);

				widget = new widgets.NullWidget(fibAtom.x, fibAtom.y, width, height);
				//writefln("NullWidget");
				//writefln("  name_fixup:0x%X", fibAtom.name_fixup);
				//writefln("  flags: %s", flagsRepr(fibAtom.flags));
				//writefln("  status: %s", fibAtom.status);
				//writefln("  type: %s", fibAtom.type);
				//writefln("  borderWidth:%s", fibAtom.borderWidth);
				//writefln("  tabstop: %s", fibAtom.tabstop);
				//writefln("  borderColor: %X", fibAtom.borderColor);
				//writefln("  contentColor: %X", fibAtom.contentColor);
				//writefln("  pos: %s, %s size: %s, %s", fibAtom.x, fibAtom.y, fibAtom.width, fibAtom.height);
				//writefln("  pData_fixup: 0x%X", fibAtom.pData_fixup);
				//writefln("  attribs_fixup: 0x%X", fibAtom.attribs_fixup);
				//writefln("  hotKeyModifiers:%s", fibAtom.hotKeyModifiers);
				//writefln("  hotKey:%s", fibAtom.hotKey);
				//writefln("  pad2:%s", fibAtom.pad2);
				//writefln("  drawstyle:%s", fibAtom.drawstyle);
				//writefln("  reserved:%s", fibAtom.reserved);
				//writefln("  pad:%s", fibAtom.pad);
			}

			if (fibAtom.flags & FAF.Link)
			{
				widget.Link = true;
				//writefln("WARNING! link: %s", widget);
			}
			if (fibAtom.flags & FAF.Function)
			{
				widget.Function = true;
				//writefln("WARNING! function: %s", widget);
			}
			assert (!(fibAtom.flags & FAF.Bitmap));
			if (fibAtom.flags & FAF.Modal)
			{
				widget.Modal = true;
			}
			if (fibAtom.flags & FAF.Popup)
			{
				widget.Popup = true;
				//writefln("WARNING! popup: %s", widget);
			}
			if (fibAtom.flags & FAF.CallOnCreate)
			{
				widget.CallOnCreate = true;
			}
			if (fibAtom.flags & FAF.ContentsVisible)
			{
				widget.ContentsVisible = true;
			}
			if (fibAtom.flags & FAF.DefaultOK)
			{
				widget.DefaultOK = true;
			}
			if (fibAtom.flags & FAF.DefaultBack)
			{
				widget.DefaultBack = true;
			}
			if (fibAtom.flags & FAF.AlwaysOnTop)
			{
				widget.AlwaysOnTop = true;
			}
			if (fibAtom.flags & FAF.Draggable)
			{
				widget.Draggable = true;
			}
			if (fibAtom.flags & FAF.BorderVisible)
			{
				widget.BorderVisible = true;
			}
			if (fibAtom.flags & FAF.Disabled)
			{
				widget.Disabled = true;
			}
			if (fibAtom.flags & FAF.DontCutoutBase)
			{
				widget.DontCutoutBase = true;
			}
			if (fibAtom.flags & FAF.CallOnDelete)
			{
				widget.CallOnDelete = true;
			}
			assert (!(fibAtom.flags & FAF.Hidden));
			if (fibAtom.flags & FAF.Background)
			{
				widget.Background = true;
			}

			widget.drawstyle = fibAtom.drawstyle;

			//convert 2-point rectangle to a 1 point/width/height

			//TODO: save x,y,w,h values in case we change resolution later...

			if (!menuItemsPresent)
			{
				if (fibAtom.flags & FAF.Background)
				{
					//feResRescaleBackground(&fibAtom);
				}
				else
				{
					if (!fibAtom.onScreen())
					{
						widget.Hidden = true;
						//writefln("WARNING! hidden: %s", widget);
					}
					//fibAtom.x = feResRepositionCentredX(fibAtom.x);
					//fibAtom.y = feResRepositionCentredY(fibAtom.y);
				}
			}
		}

		screens[screen.name] = screen;
	}
	screens.rehash;
}



// Spacer between listwindow element and the
enum
{
	LW_WindowXBarSpace = 2,
	LW_BarWidth        = 16,
	LW_BarXPos         = 10,
	LW_BarHeight       = 0,
	LW_BarYPos         = 0,
}

enum FA : ubyte
{
    UserRegion = 1,
    StaticText,
    Button,
    CheckBox,
    ToggleButton,
    ScrollBar,
    StatusBar,
    TextEntry,
    ListViewExpandButton,
    TitleBar,
    MenuItem,
    RadioButton,
    CutoutRegion,
    DecorativeRegion,
    Divider,
    ListWindow,
    BitmapButton,
    HorizSlider,
    VertSlider,
    DragButton,
    OpaqueDecorativeRegion,
}

enum FAF: uint //control flags
{
	Link               = 0x00000001,
	Function           = 0x00000002,
	Bitmap             = 0x00000004,  // unused?
	Modal              = 0x00000008,
	Popup              = 0x00000010,
	CallOnCreate       = 0x00000020,
	ContentsVisible    = 0x00000040,
	DefaultOK          = 0x00000080,
	DefaultBack        = 0x00000100,
	AlwaysOnTop        = 0x00000200,
	Draggable          = 0x00000400,
	BorderVisible      = 0x00000800,
	Disabled           = 0x00001000,
	DontCutoutBase     = 0x00002000,
	CallOnDelete       = 0x00004000,
	Hidden             = 0x00008000,  // unused?
	Background         = 0x00040000,
}
debug string flagsRepr(FAF flags)
{
	string repr;
	if (flags & FAF.Link)            repr ~= "|Link";
	if (flags & FAF.Function)        repr ~= "|Function";
	if (flags & FAF.Bitmap)          repr ~= "|Bitmap";
	if (flags & FAF.Modal)           repr ~= "|Modal";
	if (flags & FAF.Popup)           repr ~= "|Popup";
	if (flags & FAF.CallOnCreate)    repr ~= "|CallOnCreate";
	if (flags & FAF.ContentsVisible) repr ~= "|ContentsVisible";
	if (flags & FAF.DefaultOK)       repr ~= "|DefaultOK";
	if (flags & FAF.DefaultBack)     repr ~= "|DefaultBack";
	if (flags & FAF.AlwaysOnTop)     repr ~= "|AlwaysOnTop";
	if (flags & FAF.Draggable)       repr ~= "|Draggable";
	if (flags & FAF.BorderVisible)   repr ~= "|BorderVisible";
	if (flags & FAF.Disabled)        repr ~= "|Disabled";
	if (flags & FAF.DontCutoutBase)  repr ~= "|DontCutoutBase";
	if (flags & FAF.CallOnDelete)    repr ~= "|CallOnDelete";
	if (flags & FAF.Hidden)          repr ~= "|Hidden";
	if (flags & FAF.Background)      repr ~= "|Background";
	return repr.length ? repr[1..$] : repr;
}

enum FAM: uint
{
	Justification      = 0x00030000,          //mask by this to get a justification index
	JustLeft           = 0x00010000,
	JustRight          = 0x00020000,
	JustCentre         = 0x00030000,
	DropShadow         = 0x0ff00000,          //these bits not used by strings
}
//FSB_DropShadow = 20  //WTF?

enum FL : uint //FIBLinkFlags
{
    Enabled        = 1,
    DefaultPrev    = 2,
    DefaultNext    = 4,
    RetainPrevious = 8,
};



// legasy stuff

struct FibFile
{
	void[] rawdata;
	ptrdiff_t mem_offset;
	Raw[] screens;

	this(string filename) // fibfileheader *feScreensLoad(char *fileName) [src/Game/FEFlow.c]
	{
		rawdata = std.file.read(filename);
		mem_offset = cast(ptrdiff_t)rawdata.ptr;

		struct FileHeader
		{
			ubyte[8] identify;
			ushort ver;
			ushort nScreens;
		}
		FileHeader* header = cast(FileHeader*)&rawdata[0];

		scope Raw.Scr[] scrs = cast(Raw.Scr[])
			(rawdata[FileHeader.sizeof .. FileHeader.sizeof + Raw.Scr.sizeof * header.nScreens]);
		screens.length = scrs.length;
		foreach (i, ref scr; scrs)
		{
			screens[i].ptr = &scr;

			ptrdiff_t begin = cast(ptrdiff_t)scr.links_fixup;
			screens[i].links = cast(Raw.Lnk[])(rawdata[begin .. begin + Raw.Lnk.sizeof * scr.nLinks]);
			assert (screens[i].links.length == scr.nLinks);

			begin = cast(ptrdiff_t)scr.atoms_fixup;
			screens[i].atoms = cast(Raw.Atm[])(rawdata[begin .. begin + Raw.Atm.sizeof * scr.nAtoms]);
			assert (screens[i].atoms.length == scr.nAtoms);
		}
	}
	~this()
	{
		debug {(cast(byte[])rawdata)[0..$] = '0';}
		delete rawdata;
	}

	struct Raw
	{
		Scr* ptr;
		Lnk[] links;
		Atm[] atoms;

		static assert (Scr.sizeof == 20);
		struct Scr
		{
			uint name_fixup;    //name of screen for link purposes
			uint flags;         //flags for this screen
			ushort nLinks;      //number of links in this screen
			ushort nAtoms;      //number of atoms in screen
			uint links_fixup;   //pointer to list of links
			uint atoms_fixup;   //pointer to list of atoms
		}
		static assert ((Atm*).sizeof == uint.sizeof);

		static assert (Lnk.sizeof == 12);
		struct Lnk
		{
			uint name_fixup;        //optional name of this link
			FL flags;               //flags controlling behaviour of link
			char* linkToName_fixup; //name of screen to link to
		}

		static assert (Atm.sizeof == 76);
		struct Atm
		{
			uint     name_fixup;            //optional name of control
			FAF      flags;                 //flags to control behavior
			uint     status;                //status flags for this atom, checked etc.
			FA       type;                  //type of control (button, scroll bar, etc.)
			ubyte    borderWidth;           //width, in pixels, of the border
			ushort   tabstop;               //denotes the tab ordering of UI controls
			uint     borderColor;           //optional color of border
			uint     contentColor;          //optional color of content
			short    x,      loadedX;
			short    y,      loadedY;
			short    width,  loadedWidth;
			short    height, loadedHeight;
			uint     pData_fixup;  //ubyte* //pointer to type-specific data
			uint     attribs_fixup;//ubyte* //sound(button atom) or font(static text atom) reference
			ubyte    hotKeyModifiers;
			ubyte[5] hotKey;  // ubyte[FE_NumberLanguages]
			ubyte[2] pad2;
			uint[2]  drawstyle;
			uint     reserved;  //void* // region
			uint[2]  pad;

			// TEMP helpers
			bool onScreen() const
			{
				return pointOnScreen(x, y) ||
					pointOnScreen(x + width, y) ||
					pointOnScreen(x + width, y + height) ||
					pointOnScreen(x, y + height);
			}
			static bool pointOnScreen(short x, short y)
			{
				return (x >= 0) && (y >= 0) && (x < 640) && (y < 480);
			}
		}
	}
}



void main()
{
	Screen[string] screens;
	foreach (filename; ["feman/Choose_Server.fib"[],
						"feman/Construction_Manager.fib",
						"feman/CSM-ALL.fib",
						"feman/Front_End.fib",
						//"feman/front_end_demo.fib",
						"feman/Game_Chat.FIB",
						"feman/Horse_Race.fib",
						"feman/Hyperspace_Roll_Call.fib",
						"feman/In_game_esc_menu.FIB",
						"feman/Launch_Manager.FIB",
						"feman/Multiplayer_Game.fib",
						"feman/Multiplayer_LAN_Game.fib",
						"feman/Research_manager.fib",
						"feman/Sensors_manager.fib",
						"feman/single_player_objective.fib",
						"feman/TaskBar.fib",
						"feman/Trader_Interface.FIB"])
	{
		writefln("Loading %s ...", filename);
		load(filename, screens);
	}
//return;
	auto screen = screens["Main_game_screen"];
	//foreach (ref screen; screens)
	{
		writefln("\"%s\"", screen.name);
		writefln("  links:");
		foreach (ref link; screen.links)
		{
			writefln("    %s <%s>", link.name, link.target);
		}
		writefln("  atoms:");
		foreach (ref widget; screen.widgets)
		{
			writefln("    %s", widget);
		}
	}
}
