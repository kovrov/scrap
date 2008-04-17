/* Utilities for manipulating .big files of Relic Entertainment's Homeworld */

static import std.stream;
//import crc;  // relative import works?

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

/*	When decrypting filenames, don't touch the terminating null when decrypting.
	Pass in name_size, not name_size + 1. */
void decrypt_name(ubyte[] buffer) 
{ 
    ubyte last_byte = 0xD5;
    foreach (ref i; buffer) 
    { 
        last_byte ^= i; 
        i = last_byte; 
    } 
} 

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

		// test
		auto pos = _stream.position();
		foreach (TOCEntry entry; _toc)
		{
			_stream.seekSet(entry.offset);
			ubyte[] bbuffer;
			bbuffer.length = entry.nameLength;
			assert (_stream.read(bbuffer) == bbuffer.length);
			decrypt_name(bbuffer);
			writefln("entry: %s", cast(char[])bbuffer);
		}
		_stream.seekSet(pos);

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
}
