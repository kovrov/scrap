import std.stream;
import std.file;
import std.stdio;
import std.c.stdlib;


struct FibFile
{
	void[] rawdata;
	void load(string filename)
	{
		rawdata = std.file.read(filename);
		ptrdiff_t mem_offset = cast(int)&rawdata[0];

		struct FileHeader
		{
			ubyte[8] identify;
			ushort ver;
			ushort nScreens;
		}
		FileHeader* header = cast(FileHeader*)&rawdata[0];

		struct Screen
		{
			char* name;     //name of screen for link purposes
			uint flags;     //flags for this screen
			ushort nLinks;  //number of links in this screen
			ushort nAtoms;  //number of atoms in screen
			Link* links;    //pointer to list of links
			Atom* atoms;    //pointer to list of atoms
		}

		Screen[] screens = cast(Screen[])rawdata[FileHeader.sizeof .. Screen.sizeof * header.nScreens];
		foreach (ref screen; screens)
		{
			screen.name += mem_offset;
			screen.links += mem_offset;
			screen.atoms += mem_offset;
		}
	}

	struct Link
	{
		char *name;                               //optional name of this link
		uint flags;                               //flags controlling behaviour of link
		char *linkToName;                         //name of screen to link to
	}

	struct Atom
	{
		char  *name;                              //optional name of control
		uint flags;                               //flags to control behavior
		uint status;                              //status flags for this atom, checked etc.
		ubyte  type;                              //type of control (button, scroll bar, etc.)
		ubyte  borderWidth;                       //width, in pixels, of the border
		ushort  tabstop;                          //denotes the tab ordering of UI controls
		uint  borderColor;                       //optional color of border
		uint  contentColor;                      //optional color of content
		short  x,      loadedX;
		short  y,      loadedY;
		short  width,  loadedWidth;
		short  height, loadedHeight;
		ubyte *pData;                             //pointer to type-specific data
		ubyte *attribs;                           //sound(button atom) or font(static text atom) reference
		char   hotKeyModifiers;
//		char   hotKey[FE_NumberLanguages];
		char   pad2[2];
		uint drawstyle[2];
		void*  region;
		uint pad[2];
	}


}

/+
+/

void main()
{
	ubyte[] data = cast(ubyte[])"123asd".dup;
	writefln("%s", data[0..2]);
}
