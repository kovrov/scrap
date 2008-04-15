/* Utilities for manipulating .big files of Relic Entertainment's Homeworld */

static import std.stream;
import crc;  // relative import works?

const FILE_HEADER = "RBF";
const FILE_VERSION = "1.23";

/* TOC enties are serialized in .big file */
struct TOCEntry
{
    uint nameCRC1;  // first half of filename CRC 
	uint nameCRC2;  // second half of filename CRC 
    ushort nameLength; // CRCs and length are hash for filename
    uint storedLength;
    uint realLength;
    uint offset;
    int timeStamp;
    ubyte compressionType;  // bool?
} ;

class BigFile
{
	std.stream.Stream _stream;
	uint _number_of_files;
	uint _flags;
	TOCEntry[] _toc;

	this(string path)
	{
		_stream = new std.stream.File(path);

		// file signature
		ubyte[FILE_HEADER.length + FILE_VERSION.length] buffer;
		size_t read = _stream.read(buffer);
		if (read != buffer.length || buffer != cast(ubyte[])(FILE_HEADER ~ FILE_VERSION))
			throw new Exception("File signature incorrect.");

		// table of contents

		static assert (_number_of_files.sizeof == 4);  // section is 4 bytes exactly
		if (4 != _stream.readBlock(cast(void*)&_number_of_files, 4))
			throw new Exception("Reading number of files failed.");
		// TODO: fix endianness

		static assert (_flags.sizeof == 4);  // section is 4 bytes exactly
		if (4 != _stream.readBlock(cast(void*)&_flags, 4))
			throw new Exception("Reading number of files failed.");
		// TODO: fix endianness

		static assert (TOCEntry.sizeof == 32);  // each toc entry is 32 bytes exactly
		_toc.length = _number_of_files;
		foreach (ref entry; _toc)
		{
			if (32 != _stream.readBlock(cast(void*)&entry, 32))
				throw new Exception("Reading TOC entries failed.");
			// TODO: fix endianness
		}
		foreach (TOCEntry entry; _toc)
		{
			writefln("entry {%s, %s, %s, %s, %s, %s, %s, %s}",
					entry.nameCRC1, entry.nameCRC2, entry.nameLength, entry.storedLength,
					entry.realLength, entry.offset, entry.timeStamp, entry.compressionType);
		}
		//_stream.seek(, std.stream.SeekPos.Current); 
	}
	~this()
	{
		_stream.close();
	}
}


// tests
import std.stdio;
import win32.windows;

void main()
{
	char[1024] buffer;
	size_t read = GetEnvironmentVariable("HW_Data", buffer.ptr, buffer.length);
	string path = (read > 0 ? buffer[0 .. read] : ".") ~ "/update.big";

	auto scope bf = new BigFile(path);
	/*
	auto file = bf.open("AiPlayer.script");
	scope (exit) file.close();
	//interface InputStream
	//file.readLine
	foreach (line; file)
	{
		stdout.writefln("%s", line);
	}
	*/

	/* update.big:
	AiPlayer.script
	English.script
	Feman\Choose_Server.fib
	Feman\Construction_Manager.fib
	Feman\CSM-ALL.fib
	Feman\Front_End.fib
	Feman\Game_Chat.FIB
	Feman\Horse_Race.fib
	Feman\Hyperspace_Roll_Call.fib
	Feman\In_game_esc_menu.FIB
	Feman\Launch_Manager.FIB
	Feman\Multiplayer_Game.fib
	Feman\Multiplayer_LAN_Game.fib
	Feman\Research_manager.fib
	Feman\Sensors_manager.fib
	Feman\single_player_objective.fib
	Feman\TaskBar.fib
	Feman\Trader_Interface.FIB
	French.script
	German.script
	Italian.script
	R1\AdvanceSupportFrigate.shp
	R1\AttackBomber.shp
	R1\Carrier.shp
	R1\CloakedFighter.shp
	R1\HeavyCorvette.shp
	R1\HeavyDefender.shp
	R1\MinelayerCorvette.shp
	R1\Missile.shp
	R1\MissileDestroyer.shp
	R1\MultiGunCorvette.shp
	R2\AdvanceSupportFrigate.shp
	R2\AttackBomber.shp
	R2\Carrier.shp
	R2\HeavyCorvette.shp
	R2\HeavyDefender.shp
	R2\MinelayerCorvette.shp
	R2\Missile.shp
	R2\MissileDestroyer.shp
	R2\MultiGunCorvette.shp
	Spanish.script
	tweak.script
	*/
}
