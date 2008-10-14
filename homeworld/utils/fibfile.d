import std.stream;
import std.file;
import std.stdio;
import std.c.stdlib;
import std.string;

Screen[string] screens;


struct Screen
{
	string name;
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
	FibScreen[] screens;
	ptrdiff_t mem_offset;

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

		screens = cast(FibScreen[])
			rawdata[FileHeader.sizeof .. FileHeader.sizeof + FibScreen.sizeof * header.nScreens];
		foreach (ref scr; screens)
		{
			assert (scr.name_fixup !is null, "screens need a name");

			ptrdiff_t begin = cast(ptrdiff_t)scr.links_fixup;
			scr.links_fixup += mem_offset;
			foreach (ref link; cast(FibScreen.Link[])rawdata[begin .. begin + FibScreen.Link.sizeof * scr.nLinks])
			{
				//if (!(link.flags & FL.Enabled)) continue;
				assert (link.name !is null);
				link.name += mem_offset;
				assert (link.linkToName !is null);
				link.linkToName += mem_offset;
			}

			begin = cast(ptrdiff_t)scr.atoms_fixup;
			scr.atoms_fixup += mem_offset;

			/*	see if there are any menu items present in the screen so we can
				know if we should reposition the screen for high-rez */
			bool menuItemsPresent = false;
			if (scr.name_fixup == "HyperspaceRollCall")
			{
				menuItemsPresent = true;
			}
			else
			{
				foreach (ref atom; cast(FibScreen.Atom[])rawdata[begin .. begin + FibScreen.Atom.sizeof * scr.nAtoms])
				{
					if (atom.type == FA.MenuItem)
					{
						menuItemsPresent = true;
						break;
					}
				}
			}

			foreach (ref atom; cast(FibScreen.Atom[])rawdata[begin .. begin + FibScreen.Atom.sizeof * scr.nAtoms])
			{
				atom.region = null;

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

				if (atom.name) atom.name += mem_offset;

				
				if (atom.pData)
				{
					if (atom.type != FA.RadioButton) //HACK: don't fix-up radio button pointers
						atom.pData += mem_offset;

					if (atom.flags & FAF.Bitmap)  //if this is a bitmap
					{
						//...code to load in the bitmap and set new pointer
					}
					else if (atom.type != FA.RadioButton)  //else it must be a text region
					{
						atom.type = FA.StaticText;  //make it a text region
					}
				}

				if (atom.attribs)
				{
					switch (atom.type)
					{
					case FA.StaticText:
						//load in the font
						//atom.attribs = cast(ubyte*)frFontRegister(cast(char*)(atom.attribs + mem_offset));
						atom.attribs += mem_offset;
						assert (atom.attribs !is null);
						break;
					case FA.BitmapButton:
						atom.attribs += mem_offset;
						assert (atom.attribs !is null);
						break;
					}
				}
			}
		}
	}
	~this()
	{
		delete rawdata;
	}

	struct FibScreen
	{
		char* name_fixup;   //name of screen for link purposes
		uint flags;         //flags for this screen
		ushort nLinks;      //number of links in this screen
		ushort nAtoms;      //number of atoms in screen
		Link* links_fixup;  //pointer to list of links
		Atom* atoms_fixup;  //pointer to list of atoms

		struct Link
		{
			char *name;       //optional name of this link
			FL flags;         //flags controlling behaviour of link
			char *linkToName; //name of screen to link to
		}
		struct Atom
		{
			char  *name;                        //optional name of control
			FAF flags;                          //flags to control behavior
			uint status;                        //status flags for this atom, checked etc.
			FA type;                            //type of control (button, scroll bar, etc.)
			ubyte  borderWidth;                 //width, in pixels, of the border
			ushort  tabstop;                    //denotes the tab ordering of UI controls
			uint  borderColor;                  //optional color of border
			uint  contentColor;                 //optional color of content
			short  x,      loadedX;
			short  y,      loadedY;
			short  width,  loadedWidth;
			short  height, loadedHeight;
			ubyte *pData;                       //pointer to type-specific data
			ubyte *attribs;                     //sound(button atom) or font(static text atom) reference
			char   hotKeyModifiers;
			//char   hotKey[FE_NumberLanguages];
			char   pad2[2];
			uint drawstyle[2];
			void*  region;
			uint pad[2];
		}
	}
}


void load(string filename, inout Screen[string] screens)
{
	auto fib = FibFile(filename);
	foreach (ref scr; fib.screens)
	{
		Screen screen;
		screen.name = toString(scr.name_fixup + fib.mem_offset);
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
