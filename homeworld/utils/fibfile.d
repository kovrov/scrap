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



struct Atom
{
	string name;
	int width;
	int height;
	int loadedX;
	int loadedY;
	int loadedWidth;
	int loadedHeight;
	uint flags; // FAF
	ubyte type; // FA
}

struct Link
{
	string name;    //optional name of this link
	string target;  //name of screen to link to
	//FL flags;       //flags controlling behaviour of link
}

struct Screen
{
	string name;
	Atom[] atoms;
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

		assert (fibscr.ptr.name_fixup !is null, "screens need a name");
		screen.name = toString(fibscr.ptr.name_fixup + fib.mem_offset);

		screen.links.length = fibscr.links.length;
		foreach (i, ref link; screen.links)
		{
			const fiblink = &fibscr.links[i];

			if (! fiblink.flags & FL.Enabled) continue;

			assert (fiblink.name_fixup !is null);
			link.name = toString(fiblink.name_fixup + fib.mem_offset);

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

		screen.atoms.length = fibscr.atoms.length;
		foreach (i, ref atom; screen.atoms)
		{
			const fibAtom = &fibscr.atoms[i];

			assert (fibAtom.width  > fibAtom.x);
			assert (fibAtom.height > fibAtom.y);
			//convert 2-point rectangle to a 1 point/width/height
			if (fibAtom.type == FA.ListWindow)
				atom.width = fibAtom.width - (fibAtom.x + LW_BarWidth + LW_WindowXBarSpace);
			else
				atom.width = fibAtom.width - fibAtom.x;
			atom.height = fibAtom.height - fibAtom.y;
			atom.loadedX = fibAtom.x;
			atom.loadedY = fibAtom.y;
			atom.loadedWidth  = fibAtom.width;
			atom.loadedHeight = fibAtom.height;

			if (!menuItemsPresent)
			{
				if (fibAtom.flags & FAF.Background)
				{
					//feResRescaleBackground(&fibAtom);
				}
				else
				{
					//if (!feAtomOnScreen(&fibAtom))
					{
						atom.flags |= FAF.Hidden;
					}
					//fibAtom.x = feResRepositionCentredX(fibAtom.x);
					//fibAtom.y = feResRepositionCentredY(fibAtom.y);
				}
			}

			if (fibAtom.name_fixup) atom.name = toString(fibAtom.name_fixup + fib.mem_offset);

			
			if (fibAtom.pData_fixup)
			{
//				if (fibAtom.type != FA.RadioButton) //HACK: don't fix-up radio button pointers
//					fibAtom.pData_fixup + fib.mem_offset;

				if (fibAtom.flags & FAF.Bitmap)  //if this is a bitmap
				{
					//...code to load in the bitmap and set new pointer
				}
				else if (fibAtom.type != FA.RadioButton)  //else it must be a text region
				{
					atom.type = FA.StaticText;  //make it a text region
				}
			}

			if (fibAtom.attribs_fixup)
			{
				switch (fibAtom.type)
				{
				case FA.StaticText:
					//load in the font
					//fibAtom.attribs = cast(ubyte*)frFontRegister(cast(char*)(fibAtom.attribs + mem_offset));
//					fibAtom.attribs_fixup + fib.mem_offset;
					assert (fibAtom.attribs_fixup + fib.mem_offset !is null);
					break;
				case FA.BitmapButton:
//					fibAtom.attribs_fixup + fib.mem_offset;
					assert (fibAtom.attribs_fixup + fib.mem_offset !is null);
					break;
				}
			}
		}

		screens[screen.name] = screen;
	}
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
	Bitmap             = 0x00000004,
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
	Hidden             = 0x00008000,
	Background         = 0x00040000,
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
			char* name_fixup;   //name of screen for link purposes
			uint flags;         //flags for this screen
			ushort nLinks;      //number of links in this screen
			ushort nAtoms;      //number of atoms in screen
			Link* links_fixup;  //pointer to list of links
			Atom* atoms_fixup;  //pointer to list of atoms
		}

		static assert (Lnk.sizeof == 12);
		struct Lnk
		{
			char* name_fixup;       //optional name of this link
			FL flags;               //flags controlling behaviour of link
			char* linkToName_fixup; //name of screen to link to
		}

		static assert (Atm.sizeof == 76);
		struct Atm
		{
			char*    name_fixup;            //optional name of control
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
			ubyte*   pData_fixup;           //pointer to type-specific data
			ubyte*   attribs_fixup;         //sound(button atom) or font(static text atom) reference
			ubyte    hotKeyModifiers;
			ubyte[5] hotKey;  // ubyte[FE_NumberLanguages]
			ubyte[2] pad2;
			uint[2]  drawstyle;
			void*    reserved;  // region
			uint[2]  pad;
		}
	}
}



void main()
{
	Screen[string] screens;
	load("front_end.fib", screens);
	foreach (ref screen; screens)
	{
		writefln("%s", screen.name);
		writefln("  links:");
		foreach (ref link; screen.links)
		{
			writefln("    %s", link.name);
			writefln("      target: %s", link.target);
		}
		writefln("  atoms:");
		foreach (ref atom; screen.atoms)
		{
			writefln("    %s", atom.name);
		}
	}
}
