import std.stream;
import std.file;
import std.stdio;
import std.c.stdlib;
import std.string;

Screen[string] screens;


struct Atom
{
}

struct LinkTest
{
	string name;    //optional name of this link
	string target;  //name of screen to link to
//	FL flags;       //flags controlling behaviour of link
}

struct Screen
{
	string name;
	Atom[] atoms;
	LinkTest[] links;
	this(string scrname)
	{
		name = scrname;
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

struct FibFile
{
	void[] rawdata;
	ptrdiff_t mem_offset;
	FibScreen[] screens;

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

		scope FibScreen.Scr[] scrs = cast(FibScreen.Scr[])
			rawdata[FileHeader.sizeof .. FileHeader.sizeof + FibScreen.Scr.sizeof * header.nScreens];
		screens.length = scrs.length;
		foreach (i, ref scr; scrs)
		{
			screens[i].ptr = &scr;

			ptrdiff_t begin = cast(ptrdiff_t)scr.links_fixup;
			screens[i].links = cast(FibScreen.FibLink[])rawdata[begin .. begin + FibScreen.FibLink.sizeof * scr.nLinks];
			assert (screens[i].links.length == scr.nLinks);

			begin = cast(ptrdiff_t)scr.atoms_fixup;
			screens[i].atoms = cast(FibScreen.Atom[])rawdata[begin .. begin + FibScreen.Atom.sizeof * scr.nAtoms];
			assert (screens[i].atoms.length == scr.nAtoms);
		}
	}
	~this()
	{
		delete rawdata;
	}

	struct FibScreen
	{
		Scr* ptr;
		FibLink[] links;
		Atom[] atoms;

		struct Scr
		{
			char* name_fixup;   //name of screen for link purposes
			uint flags;         //flags for this screen
			ushort nLinks;      //number of links in this screen
			ushort nAtoms;      //number of atoms in screen
			FibLink* links_fixup;  //pointer to list of links
			Atom* atoms_fixup;  //pointer to list of atoms
		}

		struct FibLink
		{
			char* name_fixup;       //optional name of this link
			FL flags;               //flags controlling behaviour of link
			char* linkToName_fixup; //name of screen to link to
		}
		struct Atom
		{
			/+ char* +/ char*  name_fixup;            //optional name of control
			FAF    flags;                 //flags to control behavior
			uint   status;                //status flags for this atom, checked etc.
			FA     type;                  //type of control (button, scroll bar, etc.)
			ubyte  borderWidth;           //width, in pixels, of the border
			ushort tabstop;               //denotes the tab ordering of UI controls
			uint   borderColor;           //optional color of border
			uint   contentColor;          //optional color of content
			short  x,      loadedX;
			short  y,      loadedY;
			short  width,  loadedWidth;
			short  height, loadedHeight;
			ubyte* pData_fixup;           //pointer to type-specific data
			ubyte* attribs_fixup;         //sound(button atom) or font(static text atom) reference
			char   hotKeyModifiers;
//			char   hotKey[5];             // FE_NumberLanguages
			char   pad2[2];
			uint   drawstyle[2];
			void*  reserved; // region
			uint   pad[2];
			}
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
			auto fiblink = fibscr.links[i];
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

		foreach (ref atom; fibscr.atoms)
		{
			assert (atom.width  > atom.x);
			assert (atom.height > atom.y);
			//convert 2-point rectangle to a 1 point/width/height
			if (atom.type == FA.ListWindow)
				atom.width -= atom.x + LW_BarWidth + LW_WindowXBarSpace;
			else
				atom.width -= atom.x;

			atom.height -= atom.y;
			atom.loadedX = atom.x;
			atom.loadedY = atom.y;
			atom.loadedWidth  = atom.width;
			atom.loadedHeight = atom.height;

			if (!menuItemsPresent)
			{
				if (atom.flags & FAF.Background)
				{
					//feResRescaleBackground(&atom);
				}
				else
				{
					//if (!feAtomOnScreen(&atom))
					{
						atom.flags |= FAF.Hidden;
					}
					//atom.x = feResRepositionCentredX(atom.x);
					//atom.y = feResRepositionCentredY(atom.y);
				}
			}

			if (atom.name_fixup) toString(atom.name_fixup + fib.mem_offset);

			
			if (atom.pData_fixup)
			{
//				if (atom.type != FA.RadioButton) //HACK: don't fix-up radio button pointers
//					atom.pData_fixup + fib.mem_offset;

				if (atom.flags & FAF.Bitmap)  //if this is a bitmap
				{
					//...code to load in the bitmap and set new pointer
				}
				else if (atom.type != FA.RadioButton)  //else it must be a text region
				{
					atom.type = FA.StaticText;  //make it a text region
				}
			}

			if (atom.attribs_fixup)
			{
				switch (atom.type)
				{
				case FA.StaticText:
					//load in the font
					//atom.attribs = cast(ubyte*)frFontRegister(cast(char*)(atom.attribs + mem_offset));
//					atom.attribs_fixup + fib.mem_offset;
					assert (atom.attribs_fixup + fib.mem_offset !is null);
					break;
				case FA.BitmapButton:
//					atom.attribs_fixup + fib.mem_offset;
					assert (atom.attribs_fixup + fib.mem_offset !is null);
					break;
				}
			}
		}

		screens[screen.name] = screen;
	}
}


/+
+/

void main()
{
	load("front_end.fib", screens);
	foreach (ref screen; screens)
	{
		writefln("%s", screen.name);
	}
}
